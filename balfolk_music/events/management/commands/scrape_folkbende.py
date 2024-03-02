from datetime import datetime, timedelta

import arrow
import requests
from django.db.models import Q
from tqdm import tqdm

from balfolk_music.events.models import Event, EventDate, Festival


def fetch_from_folkbalbend(url):
    return requests.get(url, timeout=(4, 20)).json()


def get_start_timestamp(entry):
    if entry["type"] == "festival" or entry["type"] == "ball":
        if ball := entry.get("ball"):
            if ball.get("initiation_start"):
                return arrow.get("2024-01-01 " + ball.get("initiation_start")).time()
            try:
                if ball["performances"][0]["start"]:
                    return arrow.get(ball["performances"][0]["start"]).time()
                return arrow.get("2024-01-01 00:00:00").time()
            except Exception:
                return arrow.get("2024-01-01 00:00:00").time()
        return arrow.get("2024-01-01 00:00:00").time()
    if entry["type"] == "course":
        if courses := entry.get("courses"):
            return arrow.get("2024-01-01 " + courses[0]["start"]).time()
        return arrow.get("2024-01-01 00:00:00").time()

    return arrow.get("2024-01-01 00:00:00").time()


def get_end_timestamp(entry):
    if entry["type"] == "festival" or entry["type"] == "ball":
        if ball := entry.get("ball"):
            try:
                if ball["performances"][-1]["end"]:
                    return arrow.get("2024-01-01 " + ball["performances"][-1]["end"]).time()
                return arrow.get("2024-01-01 23:59:59").time()
            except Exception:
                return arrow.get("2024-01-01 23:59:59").time()
        return arrow.get("2024-01-01 23:59:59").time()
    if entry["type"] == "course":
        if courses := entry.get("courses"):
            return arrow.get("2024-01-01 " + courses[-1]["start"]).time()
        return arrow.get("2024-01-01 23:59:59").time()

    return arrow.get("2024-01-01 23:59:59").time()


def get_address(entry):
    address = entry["location"]["address"]
    s = f'{address["street"]} {address["number"]}\n{address["zip"]} {address["city"]}'
    if entry["location"].get("name"):
        s = entry["location"].get("name") + "\n\n" + s
    return s


def get_pricing(entry):
    s = ""
    for info in entry["prices"]:
        s += f'{info["name"]}: {info["price"]}\n'
    return s[:-1]


def get_description(entry):
    if entry.get("courses") and not any([entry.get("en"), entry.get("nl"), entry.get("fr")]):
        entry = entry["courses"][0]

    content = []
    if en := entry.get("en"):
        content.append("ENGLISH\n\n" + en)
    if nl := entry.get("nl"):
        content.append("NEDERLANDS\n\n" + nl)
    if fr := entry.get("fr"):
        content.append("FRANCAIS\n\n" + fr)

    return "\n\n------------------------------------\n\n".join(content)


def get_organizer(entry):
    return entry.get("organisation", {}).get("name", "")


def get_schedule(entry):
    s = ""
    if ball := entry.get("ball", {}):
        if ball["initiation_start"] and ball["initiation_end"]:
            s += ball["initiation_start"] + " - " + ball["initiation_end"] + ": Initiation" + "\n"
        elif ball["initiation_start"]:
            s += ball["initiation_start"] + ": initiation" + "\n"

        for info in ball.get("performances", []):
            if info["start"] and info["end"]:
                s += info["start"] + " - " + info["end"] + ": "
            s += info["band"]["name"] + "\n"
    return s[:-1]


def lookup_existing_festival(entry):
    date = arrow.get(entry["dates"][0])
    date_before = date.shift(days=-1)
    date_after = date.shift(days=1)

    possible_match = Festival.objects.filter(
        Q(source=Event.Source.FOLKBALBENDE) & Q(name=entry["name"]) & (Q(dates__date=date.datetime) | Q(dates__date=date_before.datetime) | Q(dates__date=date_after.datetime))
    ).first()
    return possible_match


def create_object(entry, balfolk_events_by_id):
    if " Dag " in entry["name"]:
        entry["name"] = entry["name"].split(" Dag ")[0]

    event = None
    if entry["type"] == "festival":
        event = lookup_existing_festival(entry)

    if not event:
        event = Event.objects.filter(source=Event.Source.FOLKBALBENDE, folkbende_id=entry["id"]).first()
        if not event:
            event = Event(source=Event.Source.FOLKBALBENDE, folkbende_id=entry["id"])

    event.name = entry["name"]
    event.site = entry["websites"][0]["url"] if entry["websites"] else entry.get("reservation_url", "")
    event.start_timestamp = get_start_timestamp(entry)
    event.end_timestamp = get_end_timestamp(entry)

    # Heuristic could not determine decent times, just add a few hours to the end time to be somewhat realistic
    if event.start_timestamp == event.end_timestamp:
        event.end_timestamp = (datetime.combine(arrow.get().datetime, event.end_timestamp) + timedelta(hours=3)).time()

    event.address = get_address(entry)
    event.pricing = get_pricing(entry)
    event.schedule = get_schedule(entry)
    event.organizer = get_organizer(entry)
    event.description = get_description(entry)
    event.city = entry["location"]["address"]["city"]
    event.facebook = entry.get("facebook_event", "")
    event.lattitude = entry["location"]["address"]["lat"]
    event.longitude = entry["location"]["address"]["lng"]

    if "frisse folk" in event.organizer.lower():
        event.country = "BE"
    elif any(c in event.address for c in ["Gent", "Antwerpen", "Brussel", "Bruxelles", "Mechelen", "Brugge", "Saint-Gilles"]):
        event.country = "BE"

    if entry["type"] == "ball":
        event.event_type = Event.Type.BALL
    elif entry["type"] == "festival":
        event.event_type = Event.Type.FESTIVAL
    elif entry["type"] == "course":
        event.event_type = Event.Type.COURSE
    else:
        print("unknown event type for " + str(entry))

    try:
        if event.id:
            event.save()
        else:
            event.save()
            event.save()

        dates_to_add = []
        for d in entry["dates"]:
            date_obj = EventDate.get_event_date(arrow.get(d).date())
            dates_to_add.append(date_obj)
        event.dates.set(set(dates_to_add))
        event.save()

    except Exception as e:
        print(f"error on: {entry}: {e}")


def yield_entries():
    start = arrow.get().shift(days=-2)
    end = arrow.get().shift(weeks=75)
    urls_to_do = []
    for r in arrow.Arrow.span_range("month", start, end):
        url = f"https://www.folkbalbende.be/interface/events.php?start={r[0].date()}&end={r[1].date()}&type=ball,festival,course"
        # url = f'https://www.folkbalbende.be/interface/events.php?start={r[0].date()}&end={r[1].date()}&type=festival'
        urls_to_do.append(url)

    for url in tqdm(urls_to_do[::]):
        try:
            yield from fetch_from_folkbalbend(url)
        except Exception as e:
            print(f"Error fetching url {url}: {e}")


def scrape_folkbalbende_data():
    balfolk_events_by_id = {obj.balfolknl_id: obj for obj in Event.objects.filter(source=Event.Source.BALFOLK_NL)}

    for entry in yield_entries():
        create_object(entry, balfolk_events_by_id)
