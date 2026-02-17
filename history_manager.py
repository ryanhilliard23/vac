import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self):
        self.base_dir = os.path.join('C:\\', 'VAC Downloads', 'history')
        self.history_file = os.path.join(self.base_dir, "download_history.json")
        
        # Ensure the history directory exists
        if not os.path.exists(self.base_dir):
            try:
                os.makedirs(self.base_dir)
            except Exception as e:
                print(f"[ERROR] Could not create history directory: {e}")

        self.history = self.load_history()

    def load_history(self):
        """Loads history from JSON file."""
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def add_entry(self, filename, url, fmt, size, file_path, duration="--:--", thumb_path=None, status="Completed"):
        
        # Deduplication check
        if self.history:
            top = self.history[0]
            if top.get('filename') == filename and top.get('file_path') == file_path:
                return

        entry = {
            "filename": filename,
            "url": url,
            "date": datetime.now().strftime("%b %d, %I:%M %p"),
            "format": fmt,
            "size": size,
            "file_path": file_path,
            "duration": duration,
            "thumb_path": thumb_path,
            "status": status
        }
        self.history.insert(0, entry)
        self.save_history()

    def delete_entry(self, entry_data):
        """Removes a specific entry from the history"""
        if entry_data in self.history:
            self.history.remove(entry_data)
            self.save_history()

    def save_history(self):
        """Saves current list to JSON"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Could not save history file: {e}")

    def clear_history(self):
        self.history = []
        self.save_history()
        
    def get_history(self):
        return self.history