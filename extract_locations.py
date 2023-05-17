from geotext import GeoText
import re


def extract_locations(post_text):
    location_list = []
    pattern = re.compile(r'\bto\s+([A-Za-z\s]+)')
    match = pattern.search(post_text)
    if match:
        location_text = match.group(1)
        location_words = location_text.split()
        for word in location_words:
            places = GeoText(word).cities + GeoText(word).countries
            if places:
                location_list.append(places[0])
    return location_list
