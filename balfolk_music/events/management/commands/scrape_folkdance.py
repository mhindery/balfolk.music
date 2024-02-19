import ipdb
import requests
import arrow
from tqdm import tqdm
import datetime
from balfolk_music.events.models import Event, Ball, EventDate, Festival, Course


def process_entry(entry):
    if 'start' not in entry:
        return

    event = None

    if entry.get('organisation', '') == 'balfolk.nl':
        event = Event.objects.filter(source=Event.Source.BALFOLK_NL, balfolknl_id=entry['links'][0]).first()

    elif any('folkbalbende' in l for l in entry['links']):
        f_id = 0
        for l in entry['links']:
            if 'folkbalbende' in l:
                f_id = int(l.split('/')[-1])
        event = Event.objects.filter(source=Event.Source.FOLKBALBENDE, folkbende_id=f_id).first()

    else:
        event = Event.objects.filter(
            source=Event.Source.FOLKDANCE_PAGE,
            name=entry['name'],
            folkdancepage_id=entry['name']+'_'+entry['start'],
        ).first()

    if event:
        if 'festival' in event.name.lower() or 'festival' in event.site.lower() or 'festival' in entry['name'].lower():
            event.event_type = Event.Type.FESTIVAL
        elif 'class' in event.name.lower() or 'class' in event.site.lower() or 'class' in entry['name'].lower():
            event.event_type = Event.Type.COURSE

    if not event:
        try:
            event_cls = Ball
            if 'festival' in entry['name'].lower() or 'festival' in ''.join(entry['links']).lower():
                event_cls = Festival
            elif 'class' in entry['name'].lower():
                event_cls = Course

            event = event_cls(
                source=Event.Source.FOLKDANCE_PAGE,
                folkdancepage_id=entry['name']+'_'+entry['start'],
                name=entry['name'],
                description=entry.get('details', ''),
                pricing=entry.get('price', ''),
                country=entry['country'],
                organizer=entry.get('organisation', ''),
            )
            if entry.get('organisation', '') == 'balfolk.nl' and entry['links']:
                event.balfolknl_id = entry['links'][0]
        except Exception as e:
            import ipdb
            ipdb.set_trace()
            print(e)

    event.start_timestamp = arrow.get(entry['start']).time()
    event.end_timestamp = arrow.get(entry['end']).time()
    event.starting_datetime = arrow.get(entry['start']).datetime
    event.ending_datetime = arrow.get(entry['end']).datetime

    event.city = entry['city']

    if not event.schedule:
        try:
            event.schedule = '\n'.join(entry.get('bands', []))
        except:
            import ipdb
            ipdb.set_trace()

    if entry['links']:
        event.site = entry['links'][0]
        if not event.facebook:
            for l in entry['links']:
                if 'facebook' in l:
                    event.facebook = l
                    break

    if not event.organizer:
        event.organizer = ''

    if event.country == 'UK':
        event.country = 'GB'

    try:
        if event.id:
            event.save()
        else:
            event.save()
            event.save()
    except Exception as e:
        import ipdb
        ipdb.set_trace()
        print(e)

    dates_to_add = []

    if event.event_type == Event.Type.FESTIVAL:
        for da in arrow.Arrow.range('day', arrow.get(entry['start']), arrow.get(entry['end'])):
            d, _ = EventDate.objects.get_or_create(date=da.date())
            dates_to_add.append(d)
        d, _ = EventDate.objects.get_or_create(date=arrow.get(entry['start']).date())
        dates_to_add.append(d)
        d, _ = EventDate.objects.get_or_create(date=arrow.get(entry['end']).date())
        dates_to_add.append(d)
    else:
        d, _ = EventDate.objects.get_or_create(date=arrow.get(entry['start']).date())
        dates_to_add.append(d)

    event.dates.set(set(dates_to_add))

    event.save()


def scrape_folkdance_data():
    entries = requests.get('https://folkdance.page/index.json?styles=balfolk&date=all').json()
    for entry in tqdm(entries['events'][::-1]):
        # if entry['name'] == 'Balfolk.pl Festival':
        #     import ipdb
        #     ipdb.set_trace()
        #     process_entry(entry)
        # else:
        #     continue
        process_entry(entry)
