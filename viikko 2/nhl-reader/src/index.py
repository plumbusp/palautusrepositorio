import requests
from player import Player

class PlayerReader:
    def __init__(self):
        pass

    def get_players(self, url: str) -> list[Player]:
        response = requests.get(url).json()

        players: list[Player] = []

        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players

class PlayerStats:
    def __init__(self, players: list[Player]):
        self.players = players

    def top_scorers_by_nationality(self, nationality: str):
        print(f"Players from {nationality}:")
        selected_players = selected = sorted(filter(lambda p: p.nationality == nationality, self.players), key=lambda p: p.goals + p.assists, reverse=True)

        for player in selected_players:
            if(player.nationality == nationality):
                print(f"{player.name:20} {player.team:^20} {f'{player.goals} + {player.assists} = {player.goals + player.assists}':>20}")
            


def main():
    playerReader = PlayerReader()

    players = playerReader.get_players("https://studies.cs.helsinki.fi/nhlstats/2024-25/players")

    playerStats = PlayerStats(players)
    playerStats.top_scorers_by_nationality("FIN")


if __name__ == "__main__":
    main()


