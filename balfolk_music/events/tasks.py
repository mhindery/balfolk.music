from balfolk_music.events.models import Festival, Ball, Course, Event, EventDate
import requests
import arrow
from django.db.models import Q
import json
from tqdm import tqdm

from datetime import timedelta, datetime


def fetch_from_folkbend(url):
    return requests.get(url, timeout=(2, 20)).json()


def get_start_timestamp(entry):
    # import ipdb
    # ipdb.set_trace()
    if entry['type'] == 'festival' or entry['type'] == 'ball':
        if ball := entry.get('ball'):
            if ball.get('initiation_start'):
                return ball.get('initiation_start')
            try:
                return ball['performances'][0]['start'] or arrow.get('2024-01-01 00:00:00').time()
            except:
                return arrow.get('2024-01-01 00:00:00').time()
        return arrow.get('2024-01-01 00:00:00').time()
    if entry['type'] == 'course':
        if courses := entry.get('courses'):
            return courses[0]['start']
        return arrow.get('2024-01-01 00:00:00').time()

    return arrow.get('2024-01-01 00:00:00').time()


def get_end_timestamp(entry):
    if entry['type'] == 'festival' or entry['type'] == 'ball':
        if ball := entry.get('ball'):
            try:
                return ball['performances'][-1]['end'] or arrow.get('2024-01-01 00:00:00').time()
            except:
                return arrow.get('2024-01-01 00:00:00').time()
        return arrow.get('2024-01-01 00:00:00').time()
    if entry['type'] == 'course':
        if courses := entry.get('courses'):
            return courses[-1]['start']
        return arrow.get('2024-01-01 00:00:00').time()

    return arrow.get('2024-01-01 00:00:00').time()


def get_address(entry):
    address = entry['location']['address']
    s = f'{address["street"]} {address["number"]}\n{address["zip"]} {address["city"]}'
    if entry['location'].get('name'):
        s = entry['location'].get('name') + '\n\n' + s
    return s


def get_pricing(entry):
    s = ''
    for info in entry['prices']:
        s += f'{info["name"]}: {info["price"]}\n'
    return s[:-1]


def get_description(entry):
    if entry.get('courses') and not any([entry.get('en'), entry.get('nl'), entry.get('fr')]):
        entry = entry['courses'][0]

    content = []
    if en := entry.get('en'):
        content.append('ENGLISH\n\n' + en)
    if nl := entry.get('nl'):
        content.append('NEDERLANDS\n\n' + nl)
    if fr := entry.get('fr'):
        content.append('FRANCAIS\n\n' + fr)

    return '\n\n------------------------------------\n\n'.join(content)


def get_organizer(entry):
    return entry.get('organisation', {}).get('name', '')


def get_schedule(entry):
    s = ''
    if ball := entry.get('ball', {}):
        if ball['initiation_start'] and ball['initiation_end']:
            s += ball['initiation_start'] + ' - ' + ball['initiation_end'] + ': Initiation' + '\n'
        elif ball['initiation_start']:
            s += ball['initiation_start'] + ': initiation' + '\n'

        for info in ball.get('performances', []):
            if info['start'] and info['end']:
                s += info['start'] + ' - ' + info['end'] + ': '
            s += info['band']['name'] + '\n'
    return s[:-1]


def lookup_existing_festival(entry):
    date = arrow.get(entry['dates'][0])
    date_before = date.shift(days=-1)
    date_after = date.shift(days=1)

    possible_match = Festival.objects.filter(
        Q(name=entry['name']) & (
            Q(dates__date=date.datetime) |
            Q(dates__date=date_before.datetime) |
            Q(dates__date=date_after.datetime)
        )
    ).first()
    return possible_match


def create_object(entry):
    if ' Dag ' in entry['name']:
        entry['name'] = entry['name'].split(' Dag ')[0]

    event = None
    if entry['type'] == 'festival':
        event = lookup_existing_festival(entry)

    if not event:
        event = Event.objects.filter(folkbende_id=entry['id']).first()
        if not event:
            event = Event(folkbende_id=entry['id'])

    event.name = entry['name']
    event.site = entry['websites'][0]['url'] if entry['websites'] else entry.get('reservation_url', '')
    event.start_timestamp = get_start_timestamp(entry)
    event.end_timestamp = get_end_timestamp(entry)

    if event.start_timestamp == event.end_timestamp:
        # event.end_timestamp = event.end_timestamp + timedelta(hours=2)
        # event.end_timestamp.hour += 2
        # import ipdb
        # ipdb.set_trace()
        if isinstance(event.end_timestamp, str):
            dummy = arrow.get('2022-01-01 ' + event.end_timestamp)
            event.end_timestamp = dummy.time()
        event.end_timestamp = (datetime.combine(arrow.get().datetime, event.end_timestamp) + timedelta(hours=2)).time()

    event.address = get_address(entry)
    event.pricing = get_pricing(entry)
    event.schedule = get_schedule(entry)
    event.organizer = get_organizer(entry)
    event.description = get_description(entry)
    event.city = entry['location']['address']['city']
    event.facebook = entry.get('facebook_event', '')
    event.lattitude = entry['location']['address']['lat']
    event.longitude = entry['location']['address']['lng']

    if 'frisse folk' in event.organizer.lower():
        event.country = 'BEL'

    if entry['type'] == 'ball':
        event.event_type = Event.Type.BALL
    elif entry['type'] == 'festival':
        event.event_type = Event.Type.FESTIVAL
    elif entry['type'] == 'course':
        event.event_type = Event.Type.COURSE
    else:
        print('unknown event type for ' + str(entry))

    # if event.event_type != Event.Type.COURSE:
    #     import ipdb
    #     ipdb.set_trace()

    try:
        event.save()
        # print(event)
        for d in entry['dates']:
            date_obj, _ = EventDate.objects.get_or_create(date=arrow.get(d).datetime)
            event.dates.add(date_obj)

    except Exception as e:
        import ipdb
        ipdb.set_trace()
        print(f'error on: {entry}: {e}')


def load_data_from_folkbende():
    start = arrow.get('2023-01-01')
    end = arrow.get('2024-04-01')
    urls_to_do = []
    for r in arrow.Arrow.span_range('month', start, end):
        url = f'https://www.folkbalbende.be/interface/events.php?start={
            r[0].date()}&end={r[1].date()}&type=ball,festival,course'
        # url = f'https://www.folkbalbende.be/interface/events.php?start={
        #     r[0].date()}&end={r[1].date()}&type=festival'
        urls_to_do.append(url)

    data = []
    for url in tqdm(urls_to_do):
        try:
            url_data = fetch_from_folkbend(url)
            # print(len(url_data))
            data.extend(url_data)
        except Exception as e:
            print(f'Error fetching url {url}')

    print(f'Fetched {len(data)} entries from api')
    return data


def create_from_data(data):
    for entry in tqdm(data):
        if not entry['cancelled']:
            # if entry['id'] == 2012:
            #     import ipdb
            #     ipdb.set_trace()
            create_object(entry)
