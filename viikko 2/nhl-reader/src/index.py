import requests
from player import Player
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console

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

    def top_scorers_by_nationality(self, nationality: str, season: str):
        table = Table(title=f"Season {season} - Top Scorers by Nationality: {nationality}")
        selected_players = selected = sorted(filter(lambda p: p.nationality == nationality, self.players), key=lambda p: p.goals + p.assists, reverse=True)
        table.add_column("Released", style="cyan")
        table.add_column("teams", style="magenta")
        table.add_column("goals", style="green")
        table.add_column("assists", style="yellow")
        table.add_column("points", style="red")

        for player in selected_players:
            if(player.nationality == nationality):
                table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))
        console = Console()
        console.print(table)


def main():
    season = Prompt.ask("Season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26] (2024-25):@")
    while True:
        nationality = Prompt.ask("Nationality [USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS] ():")
        playerReader = PlayerReader()

        players = playerReader.get_players(f"https://studies.cs.helsinki.fi/nhlstats/{season}/players")

        playerStats = PlayerStats(players)
        playerStats.top_scorers_by_nationality(nationality, season)


if __name__ == "__main__":
    main()


