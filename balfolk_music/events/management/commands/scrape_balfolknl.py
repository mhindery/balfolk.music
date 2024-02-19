import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import arrow
import re
from balfolk_music.events.models import Ball, Course, Event, Festival, EventDate
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_site(url):
    entry_response = requests.get(url)
    soup = BeautifulSoup(entry_response.text, 'html.parser')
    return soup


def get_timestamps(input_string):
    if input_string == 'Hele dag':
        return arrow.get('00:00', 'HH:mm').time(), arrow.get('23:59', 'HH:mm').time()
    start, end = None, None
    if '-' in input_string:
        start, end = input_string.split('-')
    start_ts = arrow.get(start, 'HH:mm')
    if end:
        end_ts = arrow.get(end, 'HH:mm')
    else:
        end_ts = start_ts.shift(hours=4)

    return start_ts.time(), end_ts.time()


def get_entry_data(url):
    # if url == 'https://www.balfolk.nl/agenda/gratis-proefles-lochem/':
    #     import ipdb
    #     ipdb.set_trace()
    try:
        soup = fetch_site(url)
        meta = soup.find(class_='meta')

        event_site_header = meta.find(class_='date')
        event_type = event_site_header.find('em').text.lower()

        if event_type == 'bal':
            event_cls = Ball
        elif event_type == 'overig':
            event_cls = Ball
        elif event_type == 'dansen leren':
            event_cls = Course
        elif event_type == 'sociales':
            event_cls = Course
        else:
            print(f'Skipping {event_type} ({url})')
            return

        date_str = event_site_header.text.split(' |')[0]
        event_date = arrow.get(date_str, 'DD-MM-YYYY').datetime

        name = meta.h2.get_text()
        description = meta.p.get_text()

        schedule = '\n'.join(a.get_text() for a in meta.find(class_="bands").find_all('a'))

        link, site, facebook = '', '', ''
        try:
            link = soup.find(string=re.compile('Meer info »')).parent.parent['href']
        except:
            pass

        if link in ['about:blank#blocked', 'https://']:
            link = ''

        if link:
            if 'facebook' in link:
                facebook = link
                site = url
            else:
                site = link
        else:
            site = url

        aanvang = soup.find(string=re.compile('Aanvang:')).parent.parent.text.replace('Aanvang:', '').strip()
        start_timestamp, end_timestamp = get_timestamps(aanvang)

        address = soup.find(string=re.compile('Locatie')).parent.parent.text.replace('Locatie: ', '').strip().replace(', ', '\n')
        if address == '\n,':
            address = ''
            city = ''
        else:
            city = address.split('\n')[-1].split(' ')[-1]
        country = 'NL'

        if soup.find(class_="lat"):
            lat = float(soup.find(class_="lat").get_text())
            lng = float(soup.find(class_="lng").get_text())
        else:
            lat = None
            lng = None

        organizer = ''
        if 'Balfolk café Nijmegen' in name:
            organizer = 'Folkbal Nijmegen'

        banner_image = ''
        for img in soup.find_all('img'):
            if img['src'].startswith('https://www.balfolk.nl/wp-content/uploads/'):
                banner_image = img['src']
                break

        pricing = soup.find(string=re.compile('Entree: ')).parent.parent.text.replace('Entree: ', '').strip()

        event = event_cls.objects.filter(source=Event.Source.BALFOLK_NL, balfolknl_id=url).first()
        if not event:
            event = event_cls(source=Event.Source.BALFOLK_NL, balfolknl_id=url)

        event.balfolknl_id = url
        event.site = url
        event.name = name
        event.description = description
        event.country = country
        event.visible = True
        event.start_timestamp = start_timestamp
        event.end_timestamp = end_timestamp
        event.address = address
        event.pricing = pricing
        event.city = city
        event.schedule = schedule
        event.lattitude = lat
        event.longitude = lng
        event.banner_image = banner_image
        event.site = site
        event.facebook = facebook
        event.organizer = organizer

        if event.id:
            event.save()
        else:
            event.save()
            event.save()

        event.dates.clear()
        d, _ = EventDate.objects.get_or_create(date=event_date)
        event.dates.add(d)
        event.save()

        print(f'Processed {event}')
    except Exception as e:
        # import ipdb
        # ipdb.set_trace()
        print(url)
        print(e)


def get_agenda_entries() -> list[str]:
    agenda_response = requests.get('https://www.balfolk.nl/agenda/')
    soup = BeautifulSoup(agenda_response.text, 'html.parser')
    entries = []
    for link in soup.find_all('a'):
        if (href := link.get('href')).startswith('https://www.balfolk.nl/agenda/'):
            if href != 'https://www.balfolk.nl/agenda/':
                yield href


def scrape_balfolknl_data():
    for entry in tqdm(get_agenda_entries()):
        get_entry_data(entry)
