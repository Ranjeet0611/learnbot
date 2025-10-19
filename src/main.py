import time
import schedule

from rich.console import Console
from learnbot.repository import repo
from learnbot.ai import ai
from learnbot.notification import notification
from learnbot.scheduler import notification_scheduler
from learnbot.constants import console_styles

console = Console(force_terminal=True)

def task():
    console.print(f"[INFO] Task triggered at {time.strftime('%Y-%m-%d %H:%M:%S')}", style=console_styles.console_blue_styles)
    try:
        daily_kafka_topic = repo.get_kafka_topics()
        ai_response = ai.get_topic_description(daily_kafka_topic['concept'])
        notification.send_notification(daily_kafka_topic['title'], ai_response)
        console.print("[SUCCESS] Task completed.", style=console_styles.console_green_styles)
    except Exception as e:
        console.print(f"[ERROR] Exception in task: {e}", style=console_styles.console_red_styles)


def main():
    notification_scheduler.schedule_daily_tech_notification(task)
    console.print("[INFO] Scheduler loop started.", style=console_styles.console_blue_styles)
    while True:
        schedule.run_pending()
        console.print(f"[DEBUG] Loop running at {time.strftime('%Y-%m-%d %H:%M:%S')}", style=console_styles.console_yellow_styles)
        time.sleep(10)

if __name__ == "__main__":
    main()
