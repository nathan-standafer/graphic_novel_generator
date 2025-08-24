import os
import glob
import subprocess
from chatterbox.tts import ChatterboxTTS
import re
import nltk
from nltk.tokenize import sent_tokenize
import torch
import torchaudio

def generate_long_audio(model, text, output_path, audio_prompt_path, max_words=80, silence_duration=0.5):
    """
    Generates long audio from text by splitting it into chunks and concatenating the results.
    Inserts silence for <br> tags.
    """
    segments = text.split('<br>')
    
    segment_audios = []

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # This is the logic to split a segment into smaller chunks.
        chunks = []
        try:
            sentences = sent_tokenize(segment)
        except LookupError:
            nltk.download('punkt')
            sentences = sent_tokenize(segment)

        chunk = ""
        for sentence in sentences:
            sentence_word_count = len(sentence.split())
            chunk_word_count = len(chunk.split())
            
            if chunk_word_count + sentence_word_count < max_words:
                chunk += " " + sentence
            else:
                if chunk:
                    chunks.append(chunk.strip())
                chunk = sentence
        if chunk:
            chunks.append(chunk.strip())
        
        # Generate audio for chunks of the segment
        audios_for_one_segment = []
        for i, chunk_text in enumerate(chunks):
            print(f"Generating audio for chunk: {chunk_text}")
            wav = model.generate(chunk_text, exaggeration=0.55, cfg_weight=0.4, audio_prompt_path=audio_prompt_path)
            audios_for_one_segment.append(wav)

        if audios_for_one_segment:
            segment_audio = torch.cat(audios_for_one_segment, -1)
            segment_audios.append(segment_audio)

    if not segment_audios:
        print("No audio generated, possibly empty text.")
        return

    # Now join with silence
    final_audio_parts = []
    
    # get silence parameters from first audio segment
    first_wav = segment_audios[0]
    sample_rate = model.sr
    
    # Ensure wav is a tensor to use .shape and .device
    if not isinstance(first_wav, torch.Tensor):
        first_wav = torch.tensor(first_wav)

    num_channels = first_wav.shape[0] if len(first_wav.shape) > 1 else 1
    device = first_wav.device
    silence_samples = int(sample_rate * silence_duration)
    
    if len(first_wav.shape) > 1:
        silence = torch.zeros((num_channels, silence_samples), device=device)
    else:
        silence = torch.zeros(silence_samples, device=device)

    for i, segment_audio in enumerate(segment_audios):
        final_audio_parts.append(segment_audio)
        if i < len(segment_audios) - 1:
            final_audio_parts.append(silence)
    
    full_audio = torch.cat(final_audio_parts, -1)
    torchaudio.save(output_path, full_audio.cpu(), sample_rate)

def generate_audio_and_srt():
    # Initialize Chatterbox TTS
    model = ChatterboxTTS.from_pretrained(device="cuda")
    AUDIO_PROMPT_PATH = "narrator_male.mp3"

    # Define directories
    source_text_dir = 'source_text_chunked'
    output_dir = 'generated_audio'
    os.makedirs(output_dir, exist_ok=True)

    # Get all chapter files
    chapter_files = sorted(glob.glob(os.path.join(source_text_dir, '*.txt')))

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
            generate_long_audio(model, text, output_audio_path, AUDIO_PROMPT_PATH)
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
                '--output_dir', output_dir #, '--highlight_words', 'True'
            ]
            print("Executing: {}".format(command))
            subprocess.run(command)
        else:
            print(f'SRT for {chapter_name} already exists.')

if __name__ == '__main__':
    generate_audio_and_srt()
