import requests
import html2text

# This script store the basic web request methods.


def requests_text(url: str) -> str:
    """
    Request text from the url.
    The return text has been removed the html tags.
    """
    r = requests.get(url)
    txt = html2text.html2text(r.text)
    return txt


def requests_photo(url: str, savepath: str):
    """
    Download photo from thr url and save it to the savepath.
    """
    try:
        r = requests.get(url)
        with open(savepath, 'wb') as f:
            f.write(r.content)
    except:
        pass
