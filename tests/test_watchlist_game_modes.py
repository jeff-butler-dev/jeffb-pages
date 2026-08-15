from pathlib import Path
import unittest

PAGE = Path(__file__).parents[1] / "site" / "watchlist" / "index.html"


def page() -> str:
    return PAGE.read_text(encoding="utf-8")


class WatchlistGameModeTests(unittest.TestCase):
    def test_games_offer_single_player_and_multiplayer_tabs(self):
        html = page()
        self.assertIn('data-game-mode="single"', html)
        self.assertIn('data-game-mode="multi"', html)
        self.assertIn('Single player', html)
        self.assertIn('Multiplayer', html)

    def test_every_game_recommendation_is_assigned_to_a_game_mode(self):
        game_lines = [line for line in page().splitlines() if '{c:"Game"' in line]
        self.assertTrue(game_lines)
        self.assertTrue(all('m:"single"' in line or 'm:"multi"' in line for line in game_lines))

    def test_multiplayer_tab_includes_new_low_barrier_social_games(self):
        html = page()
        for title in ["Helldivers 2", "Deep Rock Galactic", "The Finals"]:
            self.assertIn(f't:"{title}"', html)


if __name__ == "__main__":
    unittest.main()
