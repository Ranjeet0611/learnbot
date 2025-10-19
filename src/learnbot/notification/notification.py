from rich.console import Console
from src.learnbot.constants import console_styles
import requests

console = Console(force_terminal=True)


def send_notification(title, message):
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": "ap2rrwirrbm96t5i6qjspac1t578ka",
        "user": "usrkem1egv76ed3fbrk6z5yb7ueabb",
        "title": title,
        "message": message
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        console.print(f"[INFO] Sending notification: {title}", style=console_styles.console_blue_styles)
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            console.print("[SUCCESS] Notification sent successfully.", style=console_styles.console_green_styles)
        else:
            console.print(f"[WARNING] Notification failed with status code: {response.status_code}", style=console_styles.console_yellow_styles)
        try:
            console.print(f"[INFO] Response: {response.json()}", style=console_styles.console_blue_styles)
        except Exception as json_error:
            console.print(f"[WARNING] Could not parse response JSON: {json_error}", style=console_styles.console_yellow_styles)
    except Exception as e:
        console.print(f"[ERROR] Failed to send notification: {e}", style=console_styles.console_red_styles)
