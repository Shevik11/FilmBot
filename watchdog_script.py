import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart_script()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f'{event.src_path} has been modified, restarting script...')
            self.restart_script()

    def restart_script(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.process = subprocess.Popen([sys.executable, self.script])

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

if __name__ == "__main__":
    script = "telegramBot.py"  # Замість your_bot_script.py вкажіть назву вашого бота
    event_handler = ChangeHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler.stop()
        observer.stop()
    observer.join()
