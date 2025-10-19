import schedule
from rich.console import Console
from src.learnbot.constants import console_styles
from src.learnbot.constants import constants
console = Console(force_terminal=True)

def schedule_daily_tech_notification(task):
    try:
        schedule.every().day.at(constants.NOTIFICATION_SCHEDULE_TIME).do(task)
        console.print("[INFO] Daily tech notification scheduled at "+constants.NOTIFICATION_SCHEDULE_TIME+".", style=console_styles.console_blue_styles)
    except Exception as e:
        console.print(f"[ERROR] Failed to schedule daily tech notification: {e}", style=console_styles.console_red_styles)
