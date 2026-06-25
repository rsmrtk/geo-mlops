"""
Fetch labeled location data from OpenStreetMap via Overpass API.

Each record: (lat, lng) → location_type label
"""

import logging
import time
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

# OSM tags → our location_type labels
TAG_QUERIES = {
    "residential": 'way["landuse"="residential"]',
    "commercial":  'way["landuse"="commercial"]',
    "industrial":  'way["landuse"="industrial"]',
    "park":        'way["leisure"="park"]',
    "transport":   'node["public_transport"="station"]',
    "education":   'way["amenity"="school"]',
    "healthcare":  'way["amenity"="hospital"]',
    "religious":   'way["amenity"="place_of_worship"]',
}

# Bounding box: Ukraine
BBOX = "44.0,22.0,52.5,40.3"


@dataclass
class Sample:
    lat: float
    lng: float
    label: str


def _fetch_label(label: str, query: str, limit: int = 200) -> list[Sample]:
    overpass_query = f"""
    [out:json][timeout:25];
    (
      {query}({BBOX});
    );
    out center {limit};
    """
    headers = {"User-Agent": "geo-mlops/1.0 (https://github.com/rsmrtk/geo-mlops)"}
    for url in OVERPASS_URLS:
        try:
            resp = requests.post(url, data={"data": overpass_query},
                                 headers=headers, timeout=30)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            logger.warning("overpass error for %s at %s: %s", label, url, e)
            time.sleep(2)
    else:
        return []

    samples = []
    for el in resp.json().get("elements", []):
        if "center" in el:
            lat, lng = el["center"]["lat"], el["center"]["lon"]
        elif "lat" in el:
            lat, lng = el["lat"], el["lon"]
        else:
            continue
        samples.append(Sample(lat=lat, lng=lng, label=label))

    logger.info("fetched %d samples for %s", len(samples), label)
    return samples


def fetch_training_data(limit_per_class: int = 200) -> list[Sample]:
    all_samples: list[Sample] = []
    for label, query in TAG_QUERIES.items():
        samples = _fetch_label(label, query, limit=limit_per_class)
        all_samples.extend(samples)
        time.sleep(1)  # respect Overpass rate limit
    logger.info("total samples fetched: %d", len(all_samples))
    return all_samples
