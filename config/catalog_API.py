import requests
import difflib
import json
from pprint import pprint

url = "https://aztester.uz/api-announcement/v1/category/tree"

response_ru = requests.get(url, headers={'language': "ru"})
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})


def get_categories(response, txtmsg):
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        data = dict(json.loads(response.content))
        a = data['data']
        categories = dict()
        for i in a:
            for j in i['child_categories']:
                cat_id = j['id']
                categories[cat_id] = list()
                for e in j['child_categories']:
                    categories[cat_id].append({e['id']: e['name']})

        categories2 = set()
        for key, value in categories.items():
            for j in value:
                str1 = txtmsg.lower().split()
                str2 = list(j.values())[0].lower()

                a = difflib.get_close_matches(str2, str1, 3, 0.6)
                for i in a:
                    categories2.add(f"{key}:{list(j.values())[0]}")
        return " ".join(categories2)
    else:
        # Handle the error if the response status code is not 200 (OK)
        print("Error: ", response.status_code)

