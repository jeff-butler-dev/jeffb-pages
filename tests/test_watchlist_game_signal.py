"""Source-level guardrails for the public game-recommendations view."""
from pathlib import Path
import unittest


PAGE = Path(__file__).resolve().parents[1] / "site" / "watchlist" / "index.html"


class WatchlistGameSignalTests(unittest.TestCase):
    def setUp(self):
        self.source = PAGE.read_text(encoding="utf-8")

    def test_games_include_the_turn_based_recommendation(self):
        self.assertIn('t:"Clair Obscur: Expedition 33"', self.source)
        self.assertIn('"turn-based"', self.source)

    def test_game_category_uses_general_public_copy(self):
        self.assertIn('Character-led games for a solo night in.', self.source)
        self.assertIn('Matchmade co-op and team games chosen for lower-friction social play.', self.source)
        self.assertNotIn('built from your library', self.source.lower())

    def test_games_have_single_player_and_multiplayer_mode_tabs(self):
        self.assertIn('id="segGameMode"', self.source)
        self.assertIn('data-game-mode="single"', self.source)
        self.assertIn('data-game-mode="multi"', self.source)
        self.assertIn('m:"single"', self.source)
        self.assertIn('m:"multi"', self.source)
        self.assertIn('st.gameMode', self.source)
        self.assertIn('public-watchlist.v1', self.source)
        self.assertIn('Multiplayer', self.source)


if __name__ == "__main__":
    unittest.main()
