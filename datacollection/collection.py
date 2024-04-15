from riotwatcher import LolWatcher

REGION = 'NA1'


# Gets API key from a file in .gitignore, hiding the key.
def api_key():
    with open('../api_key.txt', 'r') as key:
        return key.read().strip()


api = LolWatcher(api_key())

# Returns array of matchIDs from the origin player
def get_origin_matchlist():
    emerald_league = api.league.entries(region=REGION, queue="RANKED_SOLO_5x5", tier="EMERALD", division="IV")
    leagueIdOfCrawlStart = emerald_league[0]['summonerId']
    print(leagueIdOfCrawlStart)
    puuidOfCrawlStart = api.summoner.by_id(region=REGION, encrypted_summoner_id=leagueIdOfCrawlStart)['puuid']
    print(puuidOfCrawlStart)
    matchlist = api.match.matchlist_by_puuid(region=REGION, puuid=puuidOfCrawlStart)
    return matchlist



