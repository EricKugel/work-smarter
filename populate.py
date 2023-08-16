from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from datetime import datetime

def populate(schedule):
    gc = GoogleCalendar("2000badbbb201fceb9770e07aaeebe18389075171628cfe4912fb70872264fc5@group.calendar.google.com", credentials_path = "./credentials/credentials.json")
    
    events = list(gc.get_events())
    print(events)

    for item in schedule:
        month, day, year = [int(thing) for thing in item[0].split("/")]
        time_start, time_end = item[1].split(" - ")
        time_start_hour, time_start_minute = [int(thing) for thing in time_start.split(":")]
        time_end_hour, time_end_minute = [int(thing) for thing in time_end.split(":")]

        event = Event("Shift", start = datetime(year, month, day, time_start_hour, time_start_minute), end = datetime(year, month, day, time_end_hour, time_end_minute))
        gc.add_event(event)