import arrow
import requests
from tqdm import tqdm

from balfolk_music.events.models import Ball, Course, Event, EventDate, Festival


def process_entry(entry, balfolk_events_by_id, folkbalbende_events_by_id, folkdancepage_events_by_id):
    new = False

    if "start" not in entry:
        return new

    event = None

    if entry.get("organisation", "") == "balfolk.nl":
        event = balfolk_events_by_id.get(entry["links"][0])

    elif any("folkbalbende" in link for link in entry["links"]):
        f_id = 0
        for link in entry["links"]:
            if "folkbalbende" in link:
                f_id = int(link.split("/")[-1])
        event = folkbalbende_events_by_id.get(f_id)

    if not event:
        event = folkdancepage_events_by_id.get(entry["name"] + "_" + arrow.get(entry["start"]).date().isoformat())

    if event:
        if "festival" in event.name.lower() or "festival" in event.site.lower() or "festival" in entry["name"].lower():
            event.event_type = Event.Type.FESTIVAL
        elif "class" in event.name.lower() or "class" in event.site.lower() or "class" in entry["name"].lower():
            event.event_type = Event.Type.COURSE

    if not event:
        try:
            event_cls = Ball
            if "festival" in entry["name"].lower() or "festival" in "".join(entry["links"]).lower():
                event_cls = Festival
            elif "class" in entry["name"].lower():
                event_cls = Course

            event = event_cls(
                source=Event.Source.FOLKDANCE_PAGE,
                folkdancepage_id=entry["name"] + "_" + arrow.get(entry["start"]).date().isoformat(),
                name=entry["name"],
                description=entry.get("details", ""),
                pricing=entry.get("price", ""),
                country=entry["country"],
                organizer=entry.get("organisation", ""),
            )
            if entry.get("organisation", "") == "balfolk.nl" and entry["links"]:
                event.balfolknl_id = entry["links"][0]
        except Exception as e:
            print(e)
            return new

        new = True

    start_dt = arrow.get(entry["start"])
    end_dt = arrow.get(entry["end"])

    event.start_timestamp = start_dt.time()
    event.end_timestamp = end_dt.time()

    event.city = entry["city"]

    if not event.schedule:
        try:
            event.schedule = "\n".join(entry.get("bands", []))
        except Exception:
            pass

    if entry["links"]:
        event.site = entry["links"][0]
        if not event.facebook:
            for link in entry["links"]:
                if "facebook" in link:
                    event.facebook = link
                    break

    if not event.organizer:
        event.organizer = ""

    if event.name.lower() == "balhalla":
        from .scrape_balhalla import update_balhalla_event

        update_balhalla_event(event)

    try:
        event.save()
    except Exception as e:
        print(e)

    dates_to_add = []

    if event.event_type == Event.Type.FESTIVAL:
        for da in arrow.Arrow.range("day", start_dt, end_dt):
            dates_to_add.append(EventDate.get_event_date(da.date()))
    else:
        dates_to_add.append(EventDate.get_event_date(start_dt.date()))

    if len(event.dates.all()) != len(dates_to_add):
        event.dates.set(set(dates_to_add))
        event.save()

    return new


def scrape_folkdance_data():
    # entries = requests.get("https://folkdance.page/index.json?styles=balfolk&date=all").json()

    folkbalbende_events_by_id = {obj.folkbende_id: obj for obj in Event.objects.filter(source=Event.Source.FOLKBALBENDE)}
    balfolknl_events_by_id = {obj.balfolknl_id: obj for obj in Event.objects.filter(source=Event.Source.BALFOLK_NL)}
    folkdancepage_events_by_id = {obj.folkdancepage_id: obj for obj in Event.objects.filter(source=Event.Source.FOLKDANCE_PAGE)}

    count = 0
    entries = requests.get("https://folkdance.page/index.json?styles=balfolk").json()
    for entry in tqdm(entries["events"]):
        if process_entry(entry, balfolknl_events_by_id, folkbalbende_events_by_id, folkdancepage_events_by_id):
            count += 1

    print(f"Processed {count} new entries")
