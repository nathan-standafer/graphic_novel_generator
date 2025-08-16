
import os
import glob
import json
import requests

def split_into_scenes(text):
    """Splits text into paragraphs, treating each as a scene."""
    return [scene.strip() for scene in text.split('\n') if scene.strip()]

def generate_prompt_for_scene(scene_text, model_name="openai/gpt-oss-20b"):
    """Generates an image prompt for a given scene using a local LLM."""
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    system_prompt = (
        "You are an expert in creating concise, descriptive prompts for an image generation model. "
        "Your prompts should vividly summarize the action, characters, and setting of the provided text. "
        "The desired art style is 'a dark, moody, 19th-century oil painting'. "
        "Do not respond with anything other than the prompt itself."
    )
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": scene_text}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        if result.get('choices') and result['choices'][0].get('message', {}).get('content'):
            return result['choices'][0]['message']['content'].strip()
        else:
            return "Error: Empty or invalid response from model."
            
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return f"Error: Could not generate prompt. {e}"

def main():
    source_text_dir = 'source_text_chunked'
    output_dir = 'generated_prompts'
    os.makedirs(output_dir, exist_ok=True)
    
    chapter_files = sorted(glob.glob(os.path.join(source_text_dir, '*.txt')))[:5]
    
    for chapter_file in chapter_files:
        chapter_name = os.path.splitext(os.path.basename(chapter_file))[0]
        output_prompt_path = os.path.join(output_dir, f'{chapter_name}_prompts.json')
        
        if os.path.exists(output_prompt_path):
            print(f"Prompts for {chapter_name} already exist. Skipping.")
            continue
            
        print(f"Processing {chapter_file}...")
        
        with open(chapter_file, 'r') as f:
            text = f.read()
            
        scenes = split_into_scenes(text)
        chapter_prompts = []
        
        for i, scene in enumerate(scenes):
            if not scene: continue
            print(f"  Generating prompt for scene {i+1}/{len(scenes)}...")
            prompt = generate_prompt_for_scene(scene)
            print(f"    - Prompt: {prompt}")
            chapter_prompts.append({
                "scene_index": i,
                "scene_text": scene,
                "image_prompt": prompt
            })
            
        with open(output_prompt_path, 'w') as f:
            json.dump(chapter_prompts, f, indent=2)
            
        print(f"Saved prompts for {chapter_name} to {output_prompt_path}")

if __name__ == '__main__':
    main()
