import json
import random

from riotwatcher import LolWatcher

REGION = 'NA1'
ROUTING_VALUE = 'AMERICAS'


# Gets API key from a file in .gitignore, hiding the key.
def api_key():
    with open('../api_key.txt', 'r') as key:
        return key.read().strip()

f = open('items.json')
data = json.load(f)


api = LolWatcher(api_key())


# Returns array of matchIDs from the origin player
def get_origin_matchlist():
    choice = random.choice(["BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"])
    emerald_league = api.league.entries(region=REGION, queue="RANKED_SOLO_5x5", tier=choice, division="IV")
    while True:
        player_index = random.randrange(0, len(emerald_league))
        leagueIdOfCrawlStart = emerald_league[player_index]['summonerId']
        puuidOfCrawlStart = api.summoner.by_id(region=REGION, encrypted_summoner_id=leagueIdOfCrawlStart)['puuid']
        puuidOfCrawlStart = api.summoner.by_id(region=REGION, encrypted_summoner_id=leagueIdOfCrawlStart)['puuid']
        matchlistOfCrawlStart = api.match.matchlist_by_puuid(region=REGION, puuid=puuidOfCrawlStart)
        match_details = api.match.by_id(match_id=matchlistOfCrawlStart[0], region='AMERICAS')
        if match_details['info']['queueId'] == 420:
            return [matchlistOfCrawlStart, puuidOfCrawlStart]


def collect_from_matchlist(matchlist):
    item_purchases_by_match = {}
    spare_matchlist = []
    for match_id in matchlist[0]:
        match_details = api.match.by_id(match_id=match_id, region='AMERICAS')
        build_by_participant = {}
        champions_by_participant = {}
        extra_puuids = []
        for participant in match_details['info']['participants']:
            champions_by_participant[participant['participantId']] = 0
            champions_by_participant[participant['participantId']] = participant['championName']
        print(match_details['info']['queueId'])

        timeline = api.match.timeline_by_match(match_id=match_id, region='AMERICAS')
        # Go through each frame in the timeline
        for frame in timeline['info']['frames']:
            # Go through each event
            for event in frame['events']:
                # Check if the event is an item purchase
                if event['type'] == 'ITEM_PURCHASED':
                    participant_id = event['participantId']
                    if champions_by_participant[participant_id] not in build_by_participant:
                        build_by_participant[champions_by_participant[participant_id]] = {}
                    item_id = event['itemId']
                    should_append = False
                    item_name = ''
                    # ensure item is a full item
                    for row in data:
                        if item_id == row['id'] and row['priceTotal'] > 2000:
                            should_append = True
                            item_name = row['name']
                    if 'build' not in build_by_participant[champions_by_participant[participant_id]]:
                        build_by_participant[champions_by_participant[participant_id]]['build'] = []
                    if should_append and len(build_by_participant[champions_by_participant[participant_id]]['build']) < 3:
                        build_by_participant[champions_by_participant[participant_id]]['build'].append(item_name)
                elif event['type'] == 'SKILL_LEVEL_UP':
                    participant_id = event['participantId']
                    if champions_by_participant[participant_id] not in build_by_participant:
                        build_by_participant[champions_by_participant[participant_id]] = {}
                    skill_slot = event['skillSlot']
                    if 'skill_order' not in build_by_participant[champions_by_participant[participant_id]]:
                        build_by_participant[champions_by_participant[participant_id]]['skill_order'] = []
                    if skill_slot not in build_by_participant[champions_by_participant[participant_id]]['skill_order'] and skill_slot != 4:
                        build_by_participant[champions_by_participant[participant_id]]['skill_order'].append(skill_slot)

        # Store the item purchase data for this match
        item_purchases_by_match[match_id] = build_by_participant
    print(item_purchases_by_match)
    collect_from_matchlist(get_origin_matchlist())


collect_from_matchlist(get_origin_matchlist())
