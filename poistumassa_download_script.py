import requests

import datetime

import json

import requests


import os

AREENA_URL = "https://areena.yle.fi"

AREENA_API_URL = "https://areena.api.yle.fi"


def get_data():
    to_download = []

    response = send_request()
    for item in response.json()["data"]:
        try:
            labels = item["labels"]
        except KeyError:
            continue
        for i in range(0, 10):
            try:
                expires = labels[i]["formatted"]
            except IndexError:
                continue

            except KeyError:
                continue
            if not expires.split(" ")[0].lower() in ["poistuu", "poistui"]:
                continue
        try:
            expire_day = expires.split(" ")[1]
        except:
            continue
        today = str(datetime.datetime.now().year) + "-" + \
            str(datetime.datetime.now().month) + \
            "-" + str(datetime.datetime.now().day)

        today = f"{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}"
        uri = item["pointer"]["uri"]
        id = uri.split("/")[-1]

        if not today == expire_day:
            continue

        uri = f"{AREENA_URL}/{id}"
        if not uri in to_download:
            to_download.append(uri)

    return to_download


def send_request():
    url = f"{AREENA_API_URL}/v1/ui/content/list"

    params = {
        'client': 'yle-areena-web',
        'language': 'fi',
        'v': '10',
        'token': 'eyJhbGciOiJIUzI1NiJ9.eyJjYXJkT3B0aW9uc1RlbXBsYXRlIjoiZXhwaXJpbmciLCJzb3VyY2UiOiJodHRwczovL3Byb2dyYW1zLmFwaS55bGUuZmkvdjMvc2NoZW1hL3YxL3BhY2thZ2VzLzMwLTI2MzkvZXhwaXJpbmciLCJhbmFseXRpY3MiOnsiY29udGV4dCI6eyJjb21zY29yZSI6eyJ5bGVfcmVmZXJlciI6InR2LnZpZXcuNTctUnl5Sm53YjliLmthaWtraV90dl9vaGplbG1hdC52aWVsYV9laGRpdC51bnRpdGxlZF9saXN0IiwieWxlX3BhY2thZ2VfaWQiOiIzMC0yNjM5In19fX0.jOr6ECwg2WKwbIayGrlxn_tDH3ebpJVp_JRAXyddWBw',
        'app_id': 'areena_web_personal_prod',
        'app_key': '6c64d890124735033c50099ca25dd2fe',
        'limit': '15',
    }

    response = requests.get(url, params=params)

    return response


to_download = get_data()
with open("to_download.txt", "w") as f:
    for down in to_download:
        f.write(down)
        f.write("\n")

os.system(
    "yle-dl -i to_download.txt --output-template '${series}/${episode_separator}-${date}' --destdir /mnt/HC_Volume_27472540/ --create-dirs")
