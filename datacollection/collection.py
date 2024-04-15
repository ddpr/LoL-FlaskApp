import json

from riotwatcher import LolWatcher

REGION = 'NA1'
ROUTING_VALUE = 'AMERICAS'


# Gets API key from a file in .gitignore, hiding the key.
def api_key():
    with open('../api_key.txt', 'r') as key:
        return key.read().strip()

f = open('items.json')
data = json.load(f)

for i in data:
    print(i['name'])


api = LolWatcher(api_key())


# Returns array of matchIDs from the origin player
def get_origin_matchlist():
    emerald_league = api.league.entries(region=REGION, queue="RANKED_SOLO_5x5", tier="EMERALD", division="IV")
    leagueIdOfCrawlStart = emerald_league[0]['summonerId']
    puuidOfCrawlStart = api.summoner.by_id(region=REGION, encrypted_summoner_id=leagueIdOfCrawlStart)['puuid']
    matchlist = api.match.matchlist_by_puuid(region=REGION, puuid=puuidOfCrawlStart)
    return matchlist


def collect_from_matchlist(matchlist):
    item_purchases_by_match = {}

    for match_id in matchlist:
        timeline = api.match.timeline_by_match(match_id=match_id, region='AMERICAS')
        items_by_participant = {}
        champions_by_participant = {}
        match_details = api.match.by_id(match_id=match_id, region='AMERICAS')
        for participant in match_details['info']['participants']:
            champions_by_participant[participant['participantId']] = 0
            champions_by_participant[participant['participantId']] = participant['championName']
        # Go through each frame in the timeline
        for frame in timeline['info']['frames']:
            # Go through each event
            for event in frame['events']:
                # Check if the event is an item purchase
                if event['type'] == 'ITEM_PURCHASED':
                    participant_id = event['participantId']
                    if champions_by_participant[participant_id] not in items_by_participant:
                        items_by_participant[champions_by_participant[participant_id]] = []
                    item_id = event['itemId']
                    should_append = False
                    for row in data:
                        if item_id == row['id'] and row['priceTotal'] > 2000:
                            should_append = True
                    if should_append and len(items_by_participant[champions_by_participant[participant_id]]) < 3:
                        items_by_participant[champions_by_participant[participant_id]].append(item_id)

        # Store the item purchase data for this match
        item_purchases_by_match[match_id] = items_by_participant
        break
    return item_purchases_by_match


print(collect_from_matchlist(get_origin_matchlist()))
