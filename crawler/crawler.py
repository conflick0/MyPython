import requests
import time
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import json


def get_card_url(url, i):
    url_list = []
    html = requests.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')
    data = sp.select("table")
    links = data[i].find_all("a")
    for link in links:
        url_list.append("https://clashroyale.fandom.com" + link.get("href"))
    return url_list


def get_card_data(url):
    card_dict = {"name:": url.split("/")[-1]}
    html = requests.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')

    results = multiple_process([get_card_table, get_card_img_url], sp)
    for r in results:
        card_dict.update(r)

    print(card_dict)
    return card_dict


def get_card_table(sp):
    dict = {}
    data = sp.select("table")
    keys = data[0].find_all("th")
    values = data[0].find_all("td")
    for key, value in zip(keys, values):
        dict.setdefault(key.text.rstrip("\n"), value.text)
    return dict


def get_card_img_url(sp):
    data = sp.select("figure")
    a = data[0].find("a")
    return {"img_url": a.get("href")}


def multiple_process(functions, args):
    results = []
    pool = ThreadPool(processes=len(functions))
    for func in functions:
        results.append(pool.apply_async(func, (args,)))
    results = [r.get() for r in results]

    pool.close()
    pool.join()
    return results


def get_card(i):
    url = "https://clashroyale.fandom.com/wiki/Cards"
    card_urls = get_card_url(url, i)

    results = []
    pool = ThreadPool(processes=len(card_urls))
    for card_url in card_urls:
        results.append(pool.apply_async(get_card_data, (card_url,)))
        time.sleep(1)

    results = [r.get() for r in results]

    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    card_lists = []
    cards = []
    types = {"troops": 0, "Defensive Buildings": 1, "Passive Buildings": 2,
             "Damaging Spells": 3, "Spawners": 4}
    for k, v in types.items():
        cards.append({k: get_card(v)})

    with open("./card.json", "w") as f:
        f.write(json.dumps(cards))
