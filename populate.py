from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.reminders import PopupReminder

from datetime import datetime

from decouple import config
from pebble import concurrent

import os

path = os.getcwd() + "/credentials"
if not os.path.isdir(path):
    os.makedirs(path)
with open("credentials/credentials.json", "w") as file:
    file.write(config("CREDENTIALS_JSON"))

@concurrent.process(timeout=120)
def create_process():
    return GoogleCalendar("2000badbbb201fceb9770e07aaeebe18389075171628cfe4912fb70872264fc5@group.calendar.google.com", credentials_path="./credentials/credentials.json")

def populate(schedule):
    try:
        try:
            process = create_process()
            gc = process.result()
        except TimeoutError:
            return "Whoops!"
        
        events = list(gc.get_events())
        all_start_times = []
        for event in events:
            start = event.start
            if isinstance(start, datetime):
                all_start_times.append((start.year, start.month, start.day, start.hour, start.minute))

        for item in schedule:
            month, day, year = [int(thing) for thing in item[0].split("/")]
            time_start, time_end = item[1].split(" - ")
            time_start_hour, time_start_minute = [int(thing) for thing in time_start.split(":")]
            time_end_hour, time_end_minute = [int(thing) for thing in time_end.split(":")]
            start = datetime(year, month, day, time_start_hour, time_start_minute)
            if start < datetime.now():
                continue
            if not (year, month, day, time_start_hour, time_start_minute) in all_start_times:
                event = Event("Eric Working (at Michael's)", start = datetime(year, month, day, time_start_hour, time_start_minute), end = datetime(year, month, day, time_end_hour, time_end_minute), reminders = [PopupReminder(minutes_before_start=60), PopupReminder(minutes_before_start=20)])
                gc.add_event(event)
    except:
        return "Whoopsy daisies!"