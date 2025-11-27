import json
import os
from datetime import datetime

CALENDAR_FILE = os.path.join(os.path.dirname(__file__), 'calendar.json')

def load_calendar_data():
    if not os.path.exists(CALENDAR_FILE):
        return {}
    with open(CALENDAR_FILE, 'r') as f:
        return json.load(f)

def save_calendar_data(data):
    with open(CALENDAR_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_tasks_for_date(date_str):
    data = load_calendar_data()
    return data.get(date_str, [])

def add_task(date_str, task_description):
    data = load_calendar_data()
    if date_str not in data:
        data[date_str] = []
    
    new_task = {
        'id': int(datetime.now().timestamp() * 1000),
        'description': task_description,
        'completed': False
    }
    data[date_str].append(new_task)
    save_calendar_data(data)
    return new_task

def update_task_status(date_str, task_id, completed):
    data = load_calendar_data()
    if date_str in data:
        for task in data[date_str]:
            if task['id'] == task_id:
                task['completed'] = completed
                save_calendar_data(data)
                return task
    return None

def delete_task(date_str, task_id):
    data = load_calendar_data()
    if date_str in data:
        original_len = len(data[date_str])
        data[date_str] = [t for t in data[date_str] if t['id'] != task_id]
        if len(data[date_str]) < original_len:
            save_calendar_data(data)
            return True
    return False