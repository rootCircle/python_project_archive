import requests
from multiprocessing.pool import ThreadPool

def url_response(url):
    path, url = url
    r = requests.get(url, stream = True)
    with open(path, 'wb') as f:
        for ch in r:
            f.write(ch)

urls = [("Event1", "https://www.python.org/events/python-events/805/"),
("Event2", "https://www.python.org/events/python-events/801/"),
("Event3", "https://www.python.org/events/python-events/790/"),
("Event4", "https://www.python.org/events/python-events/798/"),
("Event5", "https://www.python.org/events/python-events/807/"),
("Event6", "https://www.python.org/events/python-events/807/"),
("Event7", "https://www.python.org/events/python-events/757/"),
("Event8", "https://www.python.org/events/python-user-group/816/")]

ThreadPool(2).imap_unordered(url_response, urls)
