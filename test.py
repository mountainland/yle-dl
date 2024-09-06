data = [
    "https://areena.yle.fi/1-64877940",
    "https://areena.yle.fi/1-64878647",
    "https://areena.yle.fi/1-2635263",
    "https://areena.yle.fi/1-2839038",
    "https://areena.yle.fi/1-50404495",
    "https://areena.yle.fi/1-50437387",
    "https://areena.yle.fi/1-50513747",
    "https://areena.yle.fi/1-50565635",
    "https://areena.yle.fi/1-50728199",
    "https://areena.yle.fi/1-50788081",
    "https://areena.yle.fi/1-50949902",
    "https://areena.yle.fi/1-51003008",
    "https://areena.yle.fi/1-60895833",
]


def get_poistumassa(id):
    import requests

    url = f"https://areena.api.yle.fi/v1/ui/players/{id.split('/')[-1]}.json?language=fi&v=10&client=yle-areena-web&app_id=areena-web-items&app_key=v9No1mV0omg2BppmDkmDL6tGKw1pRFZt"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return str(response.json()["data"]["ondemand"]["item"]["expires"])[0:10]


for id in data:
    print(get_poistumassa(id))
