from .web_requests import requests_photo
import threading

def DownloadPhoto(results: dict, saveFolderPath: str, numOfThread: int):

    global ids
    ids = list(results.keys())

    def download_photo():
        global ids
        while len(ids) > 0:
            id = ids.pop()
            if not "photolinks" in results[id]:
                continue
            links = results[id]["photolinks"]
            order = 0
            for link in links:
                order += 1
                path = saveFolderPath + "/{}-{}.jpg".format(
                    id, order)
                requests_photo(link, path)
    
    threads = []
    for _ in range(32):
        threads.append(threading.Thread(target=download_photo))
    for t in threads:
        t.start()
    for t in threads:
        t.join()