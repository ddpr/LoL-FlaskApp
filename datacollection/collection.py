from riotwatcher import LolWatcher


# Gets API key from a file in .gitignore, hiding the key.
def api_key():
    with open('../api_key.txt', 'r') as key:
        return key.read().strip()

api = LolWatcher(api_key())
