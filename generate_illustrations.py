
import os
import json
import requests
import websocket
import uuid

def queue_prompt(prompt, client_id):
    """
    Queues a prompt on the ComfyUI server.
    """
    comfyui_url = "http://127.0.0.1:8188/prompt"
    payload = {"prompt": prompt, "client_id": client_id}
    try:
        response = requests.post(comfyui_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error queuing prompt: {e}")
        return None

def get_image(filename, subfolder, folder_type):
    """
    Gets an image from the ComfyUI server.
    """
    comfyui_url = "http://127.0.0.1:8188/view"
    params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    try:
        response = requests.get(comfyui_url, params=params)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error getting image: {e}")
        return None

def generate_images_from_prompts():
    """
    Generates images from prompts using a local ComfyUI instance.
    """
    client_id = str(uuid.uuid4())
    prompts_dir = 'generated_prompts'
    output_dir = 'generated_illustrations'
    workflow_file = 'illustration_workflow_comfyui.json'

    os.makedirs(output_dir, exist_ok=True)

    with open(workflow_file, 'r') as f:
        workflow = json.load(f)

    prompt_files = sorted([f for f in os.listdir(prompts_dir) if f.endswith('.json')])

    for prompt_file in prompt_files:
        chapter_name = os.path.splitext(prompt_file)[0].replace('_prompts', '')
        chapter_output_dir = os.path.join(output_dir, chapter_name)
        os.makedirs(chapter_output_dir, exist_ok=True)

        with open(os.path.join(prompts_dir, prompt_file), 'r') as f:
            prompts = json.load(f)

        for i, prompt_data in enumerate(prompts):
            scene_name = f"scene_{i+1:03d}"
            output_filename = f"{chapter_name}_{scene_name}.png"
            output_image_path = os.path.join(chapter_output_dir, output_filename)

            if os.path.exists(output_image_path):
                print(f"Image for {chapter_name} {scene_name} already exists. Skipping.")
                continue

            print(f"Generating image for {chapter_name} {scene_name}...")

            # Modify the workflow with the current prompt
            workflow["16"]["inputs"]["text"] = prompt_data["image_prompt"]
            workflow["9"]["inputs"]["filename_prefix"] = f"{chapter_name}_{scene_name}"

            ws = websocket.WebSocket()
            ws.connect(f"ws://127.0.0.1:8188/ws?clientId={client_id}")
            
            prompt_response = queue_prompt(workflow, client_id)
            if not prompt_response:
                ws.close()
                continue

            prompt_id = prompt_response['prompt_id']
            
            while True:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executed' and message['data']['node'] == '9' and message['data']['prompt_id'] == prompt_id:
                        data = message['data']['output']
                        for image_data in data['images']:
                            image = get_image(image_data['filename'], image_data['subfolder'], image_data['type'])
                            if image:
                                with open(output_image_path, 'wb') as f:
                                    f.write(image)
                                print(f"Saved image to {output_image_path}")
                        break
            ws.close()

if __name__ == '__main__':
    generate_images_from_prompts()
