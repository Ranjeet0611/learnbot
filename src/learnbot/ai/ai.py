from rich.console import Console
from src.learnbot.constants import console_styles, constants
import os
import requests
import json
from google import genai

console = Console(force_terminal=True)


def get_topic_description(topic_content):
    ollama_url = constants.OLLAMA_URL
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, constants.PROMPT_FILE_NAME)
    try:
        console.print("[INFO] Loading prompt template...", style=console_styles.console_blue_styles)
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
        prompt = prompt_template.replace(constants.PROMPT_TOPIC_TITLE, topic_content)
        console.print("[INFO] Sending request to AI model...", style=console_styles.console_blue_styles)
        response = requests.post(ollama_url,
                                 json={
                                     "model": constants.MODEL_NAME,
                                     "prompt": prompt,
                                     "stream": True
                                 },
                                 stream=True
                                 )
        ai_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    ai_response += data.get("response", "")
                except Exception as parse_error:
                    console.print(f"[WARNING] Error parsing line: {parse_error}",
                                  style=console_styles.console_yellow_styles)
        console.print("[SUCCESS] AI response received.", style=console_styles.console_green_styles)
        return ai_response
    except Exception as e:
        console.print(f"[ERROR] {e}", style=console_styles.console_red_styles)
        return None


def get_response_from_genai(topic_content):
    client = genai.Client()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, constants.PROMPT_FILE_NAME)
    try:
        console.print("[INFO] Loading prompt template...", style=console_styles.console_blue_styles)
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
        prompt = prompt_template.replace(constants.PROMPT_TOPIC_TITLE, topic_content)
        console.print("[INFO] Sending request to AI model...", style=console_styles.console_blue_styles)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
    except Exception as e:
        console.print(f"[ERROR] {e}", style=console_styles.console_red_styles)
        return None
    return response.text
