"""Implementation of the scraper module."""
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
    resp.raise_for_status() # <- This is a no-op if there is no HTTP error
    # remember, in requests `content` is bytes and `text` is unicode
    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    """."""
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    # Note you will have to pip install html5lib
    return parsed


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # you will likely have something different here, depending on how
        # you implemented the load_inspection_page function.
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    print(doc.prettify(encoding=encoding))
