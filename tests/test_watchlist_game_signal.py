"""Source-level guardrails for Jeff's current game-preference signal."""
from pathlib import Path
import unittest


PAGE = Path(__file__).resolve().parents[1] / "watchlist" / "index.html"


class WatchlistGameSignalTests(unittest.TestCase):
    def setUp(self):
        self.source = PAGE.read_text(encoding="utf-8")

    def test_games_reflect_expedition_33_signal(self):
        self.assertIn('t:"Clair Obscur: Expedition 33"', self.source)
        self.assertIn('t:"Metaphor: ReFantazio"', self.source)
        self.assertIn('t:"Persona 5 Royal"', self.source)
        self.assertIn('"turn-based"', self.source)

    def test_game_category_explains_the_updated_preference(self):
        self.assertIn('Expedition 33 confirmed', self.source)
        self.assertIn('live-service grinds', self.source.lower())


if __name__ == "__main__":
    unittest.main()
