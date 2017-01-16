"""Implementation of the scraper module."""

import re
import sys
import requests
from bs4 import BeautifulSoup


def get_inspection_page(**kwargs):
    """."""
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    resp.raise_for_status()  # <- This is a no-op if there is no HTTP error
    #  remember, in requests `content` is bytes and `text` is unicode
    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    """."""
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    # Note you will have to pip install html5lib
    return parsed


def extract_data_listings(html):
    """."""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(elem):
    """."""
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def extract_restaurant_metadata(elem):
    """."""
    metadata_rows = elem.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val_cell))
    return rdata


def extract_score_data(elem):
    """."""
    inspection_rows = elem.find_all(is_inspection_row)
    samples = len(inspection_rows)
    total = high_score = average = 0
    for row in inspection_rows:
        strval = clean_data(row.find_all('td')[2])
        try:
            intval = int(strval)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += intval
            high_score = intval if intval > high_score else high_score
    if samples:
        average = total / float(samples)
    data = {
        u'Average Score': average,
        u'High Score': high_score,
        u'Total Inspections': samples
    }
    return data


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)
    for listing in listings[:5]:
        metadata = extract_restaurant_metadata(listing)
        score_data = extract_score_data(listing)
        print(score_data)
