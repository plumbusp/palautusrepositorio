from index import PlayerReader, PlayerStats

url = "https://studies.cs.helsinki.fi/nhlstats/2026-27/players"
playerReader = PlayerReader()
players = playerReader.get_players(url)
stats = PlayerStats(players)

for p in stats.top_scorers_by_team("DAL"):
    print(p)