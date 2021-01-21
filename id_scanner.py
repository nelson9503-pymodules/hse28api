from .web_requests import requests_text
import threading


def GetNumOfProperties(propertyType: str = "rent") -> int:
    """
    Get the number of avalible properties.
    """
    url = "https://www.28hse.com/{}".format(propertyType)
    lines = requests_text(url).split("\n")
    for line in lines:
        if "找到了樓盤: _" in line:
            num = line.replace("找到了樓盤:", "").replace(" ", "").replace("_", "")
            return int(num)
    return 0


def ScanID(propertyType: str = "rent", numOfThread: int = 32) -> list:
    """
    Scan all the properties id avalible on 28 House.

    propertyType -> "rent" or "buy"
    """
    global properties
    global page
    properties = {}
    page = 0
    coverurl = "https://www.28hse.com/{}/list-".format(propertyType)

    def scan_page():
        global page
        global properties
        while True:
            page += 1
            url = coverurl + str(page)
            txt = requests_text(url)
            if not "https://www.28hse.com/{}-property-".format(propertyType) in txt:
                break
            txt = txt.split(
                "https://www.28hse.com/{}-property-".format(propertyType))
            for i in range(1, len(txt)):
                if ".html" in txt[i]:
                    id = txt[i].split(".html")[0]
                    properties[id] = 0

    threads = []
    for _ in range(numOfThread):
        threads.append(threading.Thread(target=scan_page))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    ids = []
    for id in properties:
        ids.append(id)

    return ids
