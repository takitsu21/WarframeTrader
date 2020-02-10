import json


def locales(lang="en"):
    with open("locales/" + lang + ".json", "r", encoding="utf8") as f:
        datastore = json.load(f)
    return datastore

if __name__ == "__main__":
    print(locales("fr"))