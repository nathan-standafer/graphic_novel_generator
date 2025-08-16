import os
import glob
import subprocess
from whisperspeech.pipeline import Pipeline
import re
import nltk
from nltk.tokenize import sent_tokenize
import torch
import torchaudio

def split_and_prepare_text(text, cps=14):
    chunks = []
    try:
        sentences = sent_tokenize(text)
    except LookupError:
        nltk.download('punkt')
        try:
            sentences = sent_tokenize(text)
        except LookupError:
            nltk.download('punkt_tab')
            sentences = sent_tokenize(text)

    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < 20 * cps:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def generate_long_audio(pipe, text, output_path, speaker=None, cps=14):
    """
    Generates long audio from text by splitting it into chunks and concatenating the results.
    """
    chunks = split_and_prepare_text(text, cps=cps)
    
    audios = []
    for i, chunk in enumerate(chunks):
        print(f"Generating audio for chunk {i+1}/{len(chunks)}...")
        audio_tensor = pipe.generate(chunk, speaker=speaker, lang='en', cps=cps)
        audios.append(audio_tensor)

    if audios:
        full_audio = torch.cat(audios, -1)
        torchaudio.save(output_path, full_audio.cpu(), 24000)

def generate_audio_and_srt():
    # Initialize WhisperSpeech pipeline
    pipe = Pipeline(s2a_ref='collabora/whisperspeech:s2a-q4-base-en+pl.model')

    # Define directories
    source_text_dir = 'source_text_chunked'
    output_dir = 'generated_audio'
    os.makedirs(output_dir, exist_ok=True)

    # Get all chapter files
    chapter_files = sorted(glob.glob(os.path.join(source_text_dir, '*.txt')))[:5]

    for chapter_file in chapter_files:
        chapter_name = os.path.splitext(os.path.basename(chapter_file))[0]
        output_audio_path = os.path.join(output_dir, f'{chapter_name}.wav')
        output_srt_path = os.path.join(output_dir, f'{chapter_name}.srt')

        print(f'Processing {chapter_file}...')

        # Read chapter text
        with open(chapter_file, 'r') as f:
            text = f.read()

        # Generate audio
        if not os.path.exists(output_audio_path):
            print(f'Generating audio for {chapter_name}...')
            generate_long_audio(pipe, text, output_audio_path)
        else:
            print(f'Audio for {chapter_name} already exists.')

        # Generate SRT
        if not os.path.exists(output_srt_path):
            print(f'Generating SRT for {chapter_name}...')
            command = [
                'conda', 'run', '-n', 'openhands', 'python', '-m', 'whisperx',
                output_audio_path,
                '--model', 'large-v2',
                '--output_format', 'srt',
                '--output_dir', output_dir
            ]
            subprocess.run(command)
        else:
            print(f'SRT for {chapter_name} already exists.')

if __name__ == '__main__':
    generate_audio_and_srt()