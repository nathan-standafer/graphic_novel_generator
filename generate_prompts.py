import os
import glob
import json
import re
import requests
import time

def parse_srt_into_segments(srt_content):
    """Parses SRT file content into a list of dialogue segments."""
    # This regex finds all text blocks, stripping timestamps and indices
    text_blocks = re.findall(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*?)(?=\n\n\d+\n|\Z)', srt_content, re.DOTALL)
    
    # Clean up each block by removing extra whitespace and newlines
    cleaned_blocks = [re.sub(r'\s+', ' ', block.strip()) for block in text_blocks]
    return cleaned_blocks


def generate_prompt_for_scene(scene_text, character_list, chapter_context=None, model_name="openai/gpt-oss-20b", retries=3, backoff_factor=0.5):
    """Generates an image prompt for a given scene using a local LLM with chapter context."""
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    system_prompt = (
        "You are an expert in creating concise, descriptive prompts for an image generation model. "
        "Your task is to generate vivid, detailed image prompts based on specific scenes from a chapter of the novel, Moby Dick. "
        "Use the provided chapter context and character list to understand the narrative style, setting, and characters involved. "
        "You will be given a sentence from the chapter (Sentence to Illustrate). Your prompts should vividly summarize the action, characters, and setting taking place when the specified sentence is read. "
        #"The desired art style is 'a dark, moody, 19th-century oil painting'. "
        "The desired art style is a moody, high‑contrast image in Romantic realism with deep navy and charcoal tones, sharp chiaroscuro lighting, fine linework blended with semi‑realistic gradients, and subtle paper grain—capturing the tension of a 19th‑century whaling voyage."
        "Do not respond with anything other than the prompt itself. "
        "Limit the prompt to 70 words. The prompt must always specify the desired art style and time period."
    )

    # Sanitize and truncate scene_text
    scene_text = re.sub(r'[^\w\s.,-]', '', scene_text)
    if len(scene_text) > 20000:
        scene_text = scene_text[:20000] + " [truncated]"

    # Prepare the user message with context, characters, and the specific scene
    user_content = ""
    if chapter_context:
        context_summary = chapter_context[:40000]
        if len(chapter_context) > 40000:
            context_summary += " [truncated for brevity]"
        user_content += f"Chapter Context: {context_summary}\n\n"
    
    if character_list:
        user_content += f"Key Characters: {', '.join(character_list)}\n\n"

    user_content += f"Sentence to Illustrate: {scene_text}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

    data = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 350
    }

    print(data)

    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            if result.get('choices') and result['choices'][0].get('message', {}).get('content'):
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"Warning: Empty or invalid response on attempt {attempt + 1}.")
        
        except requests.exceptions.RequestException as e:
            print(f"API request failed on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))
            else:
                return f"Error: Could not generate prompt after {retries} attempts. {e}"
    
    return "Error: Failed to generate prompt after multiple retries."

def main():
    source_audio_dir = 'generated_audio'
    output_dir = 'generated_prompts'
    os.makedirs(output_dir, exist_ok=True)

    # Hardcoded character list for Moby Dick
    character_list = ["Captain Ahab", "Ishmael", "Queequeg", "Starbuck", "Stubb", "Flask", "Moby Dick"]

    chapter_files = sorted(glob.glob(os.path.join(source_audio_dir, '*.srt')))

    for chapter_file in chapter_files:
        chapter_name = os.path.splitext(os.path.basename(chapter_file))[0]
        output_prompt_path = os.path.join(output_dir, f'{chapter_name}_prompts.json')

        if os.path.exists(output_prompt_path):
            overwrite = input(f"Prompts for {chapter_name} already exist. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print(f"Skipping {chapter_name}.")
                continue

        print(f"Processing {chapter_file}...")

        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                srt_content = f.read()
        except FileNotFoundError:
            print(f"Error: {chapter_file} not found. Skipping.")
            continue

        segments = parse_srt_into_segments(srt_content)
        full_chapter_text = ' '.join(segments)
        chapter_prompts = []

        for i, segment in enumerate(segments):
            if not segment.strip():
                continue
            
            print(f"  Generating prompt for segment {i+1}/{len(segments)}...")
            prompt = generate_prompt_for_scene(segment, character_list, chapter_context=full_chapter_text)
            
            if "Error:" in prompt:
                print(f"    - {prompt}")
            else:
                print(f"    - Segment: {segment}")
                print(f"    - Prompt: {prompt}\n")

            chapter_prompts.append({
                "segment_index": i,
                "segment_text": segment,
                "image_prompt": prompt
            })

        with open(output_prompt_path, 'w', encoding='utf-8') as f:
            json.dump(chapter_prompts, f, indent=2, ensure_ascii=False)

        print(f"Saved prompts for {chapter_name} to {output_prompt_path}")

if __name__ == '__main__':
    main()
