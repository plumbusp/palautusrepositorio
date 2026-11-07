import requests
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from player import Player


class PlayerReader:
    def get_players(self, url: str) -> list[Player]:
        response = requests.get(url, timeout=10).json()

        return [Player(player_dict) for player_dict in response]


class PlayerStats:
    def __init__(self, players: list[Player]):
        self.players = players

    def top_scorers_by_nationality(
        self, nationality: str, season: str
    ) -> None:
        selected_players = sorted(
            (player for player in self.players
             if player.nationality == nationality),
            key=lambda player: player.goals + player.assists,
            reverse=True,
        )
        table = Table(
            title=(
                f"Season {season} - Top Scorers by Nationality: "
                f"{nationality}"
            )
        )
        table.add_column("Released", style="cyan")
        table.add_column("teams", style="magenta")
        table.add_column("goals", style="green")
        table.add_column("assists", style="yellow")
        table.add_column("points", style="red")

        for player in selected_players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.goals + player.assists),
            )
        Console().print(table)


def main() -> None:
    season = Prompt.ask(
        "Season [2018-19/2019-20/2020-21/2021-22/2022-23/"
        "2023-24/2024-25/2025-26] (2024-25):@"
    )
    while True:
        nationality = Prompt.ask(
            "Nationality [USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/"
            "DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS] ():"
        )
        player_reader = PlayerReader()

        players = player_reader.get_players(
            f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
        )

        player_stats = PlayerStats(players)
        player_stats.top_scorers_by_nationality(nationality, season)


if __name__ == "__main__":
    main()
