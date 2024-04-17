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
item_json = json.load(f)
f.close()
f = open('runesReforged.json')
runes_json = json.load(f)
f.close()

api = LolWatcher(api_key())


# Returns array of matchIDs from the origin player
def get_origin_matchlist():
    choice = random.choice(["BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"])
    emerald_league = api.league.entries(region=REGION, queue="RANKED_SOLO_5x5", tier=choice, division="IV")
    while True:
        player_index = random.randrange(0, len(emerald_league))
        leagueIdOfCrawlStart = emerald_league[player_index]['summonerId']
        puuidOfCrawlStart = api.summoner.by_id(region=REGION, encrypted_summoner_id=leagueIdOfCrawlStart)['puuid']
        matchlistOfCrawlStart = api.match.matchlist_by_puuid(region=REGION, puuid=puuidOfCrawlStart)
        match_details = api.match.by_id(match_id=matchlistOfCrawlStart[0], region='AMERICAS')
        if match_details['info']['queueId'] == 420:
            return [matchlistOfCrawlStart, puuidOfCrawlStart]

def get_participant_champions(match_details):
    champions_by_participant = {}
    for participant in match_details['info']['participants']:
        participant_id = participant['participantId']
        champions_by_participant[participant_id] = participant['championName']
        #participant_champion = 0
        #participant_champion = participant['championName']
    return champions_by_participant

def get_items_and_skillorder(timeline, champions_by_participant):
    build_by_participant = {}
    # Go through each frame in the timeline
    for frame in timeline['info']['frames']:
        # Go through each event
        for event in frame['events']:
            # Check if the event is an item purchase
            if event['type'] == 'ITEM_PURCHASED':
                participant_id = event['participantId']
                participant_champion = champions_by_participant[participant_id]
                if participant_champion not in build_by_participant:
                    build_by_participant[participant_champion] = {}
                item_id = event['itemId']
                should_append = False
                item_name = ''
                # ensure item is a full item
                for row in item_json:
                    if item_id == row['id'] and row['priceTotal'] > 2000:
                        should_append = True
                        item_name = row['name']
                if 'build' not in build_by_participant[participant_champion]:
                    build_by_participant[participant_champion]['build'] = []
                if should_append and len(
                        build_by_participant[participant_champion]['build']) < 3:
                    build_by_participant[participant_champion]['build'].append(item_name)
            elif event['type'] == 'SKILL_LEVEL_UP':
                participant_id = event['participantId']
                participant_champion = champions_by_participant[participant_id]
                if participant_champion not in build_by_participant:
                    build_by_participant[champions_by_participant[participant_id]] = {}
                skill_slot = event['skillSlot']
                if 'skill_order' not in build_by_participant[participant_champion]:
                    build_by_participant[participant_champion]['skill_order'] = []
                if skill_slot not in build_by_participant[participant_champion]['skill_order'] and skill_slot != 4:
                    build_by_participant[champions_by_participant[participant_id]]['skill_order'].append(skill_slot)
    return build_by_participant

def get_runes(match_details, build_by_participant, champions_by_participant):
    for participant in match_details['info']['participants']:
        participant_id = participant['participantId']
        participant_champion = champions_by_participant[participant_id]
        build_by_participant[participant_champion]['runes'] = []
        styles = participant['perks']['styles']
        PRIMARY_STYLE = 0
        SECONDARY_STYLE = 1
        # Get Primary Tree Runes
        for i in range(0, 4):
            rune_id = styles[PRIMARY_STYLE]['selections'][i]['perk']
            tree_id = styles[PRIMARY_STYLE]['style']
            #print(rune_id)
            for row in runes_json:
                if row['id'] != tree_id:
                    continue
                for rune in row['slots'][i]['runes']:
                    if rune['id'] == rune_id:
                        rune_name = rune['key']
            build_by_participant[participant_champion]['runes'].append(rune_name)
        for i in range(0, 2):
            rune_id = styles[SECONDARY_STYLE]['selections'][i]['perk']
            tree_id = styles[SECONDARY_STYLE]['style']
            print(rune_id)
            for row in runes_json:
                if row['id'] != tree_id:
                    continue
                for slot_row in row['slots']:
                    for rune in slot_row['runes']:
                        if rune['id'] == rune_id:
                            rune_name = rune['key']
            build_by_participant[participant_champion]['runes'].append(rune_name)



def collect_from_matchlist(matchlist):
    item_purchases_by_match = {}
    for match_id in matchlist[0]:
        match_details = api.match.by_id(match_id=match_id, region='AMERICAS')
        if match_details['info']['queueId'] != 420:
            break
        champions_by_participant = get_participant_champions(match_details)
        timeline = api.match.timeline_by_match(match_id=match_id, region='AMERICAS')
        build_by_participant = get_items_and_skillorder(timeline, champions_by_participant)
        get_runes(match_details, build_by_participant, champions_by_participant)
        # Store the item purchase data for this match
        print(build_by_participant)
        item_purchases_by_match[match_id] = build_by_participant
    print(len(item_purchases_by_match))
    print(item_purchases_by_match)
    collect_from_matchlist(get_origin_matchlist())


collect_from_matchlist(get_origin_matchlist())
