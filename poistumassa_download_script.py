import requests

import datetime

import json

import time

import os

def get_poistumassa(id):
    import requests

    url = f"https://areena.api.yle.fi/v1/ui/players/{id}.json?language=fi&v=10&client=yle-areena-web&app_id=areena-web-items&app_key=v9No1mV0omg2BppmDkmDL6tGKw1pRFZt"

    payload={}
    headers = {
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return (str(response.json()["data"]["ondemand"]["item"]["expires"])[0:10])


from bs4 import BeautifulSoup
soup = BeautifulSoup(requests.get(
    "https://areena.yle.fi/tv/ohjelmat/kaikki?t=viela_ehdit").text, 'html.parser')

tokens = []

for item in soup.find_all("div", {"class": "package-view"}):
    cont = json.loads(item["data-view"])
    cont = cont["tabs"]
    
    for item in cont[0]["content"]:
        if not item["source"]["authentication"] == ['yle-api']:
            continue

        uri = (item["source"]["uri"])

        if not ("https://areena.api.yle.fi/v1/ui/content/list?client=yle-areena-web") in uri:
            continue

        uri = uri.split("&")
        for uri1 in uri:
            if not uri1.startswith("token"):
                continue
            token = (uri1.replace("token=", ""))
            tokens.append(token)


AREENA_URL = "https://areena.yle.fi"

def test_token(token):
    client = "yle-areena-web"

    language = "fi"

    v = "10"

    app_id = "areena_web_personal_prod"

    app_key = "6c64d890124735033c50099ca25dd2fe"

    limit = "15"

    url = f"https://areena.api.yle.fi/v1/ui/content/list?client={client}&language={language}&v={v}&token={token}&app_id={app_id}&app_key={app_key}&limit={limit}"

    try:
        response = requests.request(
                "GET", url, headers=headers, data=payload)

        return True
    except:
        return False
    
def get_data(tokens):
    client = "yle-areena-web"

    language = "fi"

    v = "10"

    app_id = "areena_web_personal_prod"

    app_key = "6c64d890124735033c50099ca25dd2fe"

    limit = "15"
    to_download = []

    for token in tokens:
        print(token)
        try:
            response = send_request(client, language, v, app_id, app_key, limit, token)
        except:
            continue
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
            today = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
            
            today1 = f"{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}"

            today = today1

            uri = item["pointer"]["uri"]
            id = uri.split("/")[-1]



            if not today == expire_day:
                continue



            uri = f"{AREENA_URL}/{id}"
            if not uri in to_download:
                to_download.append(uri)
            

    return to_download

def send_request(client, language, v, app_id, app_key, limit, token):
    response = requ()
    # return response FIX: If doenst work, uncomment
    url = "https://areena.api.yle.fi/v1/ui/content/list"

    params = {
        'client': client,
        'language': language,
        'v': v,
        'token': token,
        'app_id': app_id,
        'app_key': app_key,
        'limit': limit,
    }


    response = requests.get(url, params=params)
        
    return response

def requ():
    import requests

    params = {
        'client': 'yle-areena-web',
        'language': 'fi',
        'v': '10',
        'token': 'eyJhbGciOiJIUzI1NiJ9.eyJjYXJkT3B0aW9uc1RlbXBsYXRlIjoiZXhwaXJpbmciLCJzb3VyY2UiOiJodHRwczovL3Byb2dyYW1zLmFwaS55bGUuZmkvdjMvc2NoZW1hL3YxL3BhY2thZ2VzLzMwLTI2MzkvZXhwaXJpbmciLCJhbmFseXRpY3MiOnsiY29udGV4dCI6eyJjb21zY29yZSI6eyJ5bGVfcmVmZXJlciI6InR2LnZpZXcuNTctUnl5Sm53YjliLmthaWtraV90dl9vaGplbG1hdC52aWVsYV9laGRpdC51bnRpdGxlZF9saXN0IiwieWxlX3BhY2thZ2VfaWQiOiIzMC0yNjM5In19fX0.jOr6ECwg2WKwbIayGrlxn_tDH3ebpJVp_JRAXyddWBw',
        'app_id': 'areena_web_personal_prod',
        'app_key': '6c64d890124735033c50099ca25dd2fe',
        'limit': '15',
    }

    response = requests.get('https://areena.api.yle.fi/v1/ui/content/list', params=params)

    return response

def get_thing(labels):
    cont = False
    for i in range(0, 10):
        try:
            expires = labels[i]["formatted"]
            cont = False
        except IndexError:
            expires = None
            continue
                
        except KeyError:
            continue
        if not expires.split(" ")[0].lower() in ["poistuu", "poistui"]:
            cont = True
            continue
    return cont,expires


to_download = get_data(tokens)
with open("to_download.txt", "w") as f:
    for down in to_download:
        f.write(down)
        f.write("\n")

import os
os.system("yle-dl -i to_download.txt --output-template '${series}/${episode_separator}-${date}' --destdir /mnt/HC_Volume_27472540/ --create-dirs")
