import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from balfolk_music.events.models import Event


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_site(url):
    entry_response = requests.get(url)
    soup = BeautifulSoup(entry_response.text, "html.parser")
    return soup


def update_balhalla_event(event: Event):
    # import ipdb
    # ipdb.set_trace()
    try:
        soup = fetch_site(event.site)
    except Exception:
        return

    try:
        event.description = soup.find(property="og:description")["content"].strip()
        event.address = soup.find("address").text.strip(" \n")
        event.pricing = soup.find(class_="table-auto w-full md:w-2/3 lg:w-1/2").text.replace("\n\n\n\n", "\n").replace("\n\n\n", "\n\n").strip(" \n")
        event.schedule = soup.find("ol").text.replace("\n–\n", " ").replace("\n\n", " ").strip(" \n")
    except Exception as e:
        print("error on parsing balhalla: ", e)

    if "paulushuis" in event.address.lower():
        event.lattitude = 51.0396194
        event.longitude = 3.7058035
