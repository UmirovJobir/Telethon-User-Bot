import requests
import difflib
import json
from pprint import pprint

url = "https://aztester.uz/api-announcement/v1/category/tree"

response_ru = requests.get(url, headers={'language': "ru"})
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})


def get_categories(response, message):
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        data = dict(json.loads(response.content))
        a = data['data']
        categories = dict()
        for i in a:
            for j in i['child_categories']:
                cat_id = j['name']
                
                if len(j['child_categories']) == 0:
                    parent_cat = i['name']
                    if categories.get(parent_cat) is None:
                        categories[parent_cat] = list()
                        categories[parent_cat].append({j['id']: j['name']})
                    else:
                        categories[parent_cat].append({j['id']: j['name']})
                else:
                    categories[cat_id] = list()
                    for e in j['child_categories']:
                        categories[cat_id].append({e['id']: e['name']})

        categories2 = set()

        message_list = message.lower().split()

        for key, value in categories.items():
            for j in value:
                str2 = list(j.values())[0].lower()
                a = difflib.get_close_matches(str2, message_list, 3, 0.6)   
                for i in a:
                    categories2.add(f"{key}:{list(j.values())[0]}")
        return ", ".join(categories2)
    else:
        # Handle the error if the response status code is not 200 (OK)
        print("Error: ", response.status_code)

