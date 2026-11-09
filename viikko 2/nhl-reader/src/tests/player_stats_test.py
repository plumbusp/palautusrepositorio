"""Unit tests for PlayerStats."""

from io import StringIO
import unittest
from unittest.mock import patch

from rich.console import Console as RichConsole

# The application modules are in the sibling src directory.
# pylint: disable=import-error
from index import PlayerReader, PlayerStats
from player import Player


# pylint: disable=too-few-public-methods
class StubPlayerReader(PlayerReader):
    """Return local test players instead of making an HTTP request."""

    def get_players(self, url: str) -> list[Player]:
        """Return deterministic players for the tests."""
        del url
        return [
            Player({
                "name": "Alex Barkov",
                "nationality": "FIN",
                "assists": 30,
                "goals": 30,
                "team": "FLA",
                "games": 80,
            }),
            Player({
                "name": "Sebastian Aho",
                "nationality": "FIN",
                "assists": 35,
                "goals": 25,
                "team": "CAR",
                "games": 80,
            }),
            Player({
                "name": "Mikko Rantanen",
                "nationality": "FIN",
                "assists": 40,
                "goals": 35,
                "team": "COL",
                "games": 80,
            }),
            Player({
                "name": "Patrik Laine",
                "nationality": "FIN",
                "assists": 30,
                "goals": 40,
                "team": "CBJ",
                "games": 80,
            }),
            Player({
                "name": "Aleksander Barkov",
                "nationality": "RUS",
                "assists": 60,
                "goals": 50,
                "team": "FLA",
                "games": 80,
            }),
        ]


class TestPlayerStats(unittest.TestCase):
    """Test PlayerStats using players from a local reader stub."""

    def setUp(self):
        """Create statistics from the stubbed player data."""
        reader = StubPlayerReader()
        self.stats = PlayerStats(reader.get_players("stub://players"))

    def test_top_scorers_by_team_returns_only_team_players_in_goal_order(self):
        """Return only players from the requested team in goal order."""
        players = self.stats.top_scorers_by_team("FLA")

        self.assertEqual(
            [player.name for player in players],
            ["Aleksander Barkov", "Alex Barkov"],
        )

    def test_top_goal_scorers_returns_requested_number_in_goal_order(self):
        """Return the requested number of players in goal order."""
        players = self.stats.top_goal_scorers(3)

        self.assertEqual(
            [player.name for player in players],
            ["Aleksander Barkov", "Patrik Laine", "Mikko Rantanen"],
        )

    @patch("index.Console")
    def test_top_scorers_by_nationality_prints_limited_points_order(self, console):
        """Print nationality results ordered by points and limited in count."""
        output = StringIO()
        console.return_value = RichConsole(file=output, color_system=None)

        result = self.stats.top_scorers_by_nationality("FIN", "2025-26", 2)

        self.assertIsNone(result)
        rendered = output.getvalue()
        self.assertLess(
            rendered.index("Mikko Rantanen"),
            rendered.index("Patrik Laine"),
        )
        self.assertNotIn("Alex Barkov", rendered)


if __name__ == "__main__":
    unittest.main()
