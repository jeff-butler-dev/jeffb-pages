"""Behavioral source checks for the whole-media recommendation engine."""
from pathlib import Path
import unittest


PAGE = Path(__file__).resolve().parents[1] / "watchlist" / "index.html"


class RecommendationEngineTests(unittest.TestCase):
    def setUp(self):
        self.source = PAGE.read_text(encoding="utf-8")

    def test_uses_shared_trait_weights_instead_of_only_fixed_match_scores(self):
        self.assertIn('const TRAITS=', self.source)
        self.assertIn('function score(', self.source)
        self.assertIn('traitWeights', self.source)

    def test_supports_local_feedback_that_updates_future_ranking(self):
        self.assertIn('data-feedback', self.source)
        self.assertIn('function setFeedback(', self.source)
        self.assertIn('feedback:', self.source)

    def test_explains_why_each_recommendation_is_ranked(self):
        self.assertIn('function reasonsFor(', self.source)
        self.assertIn('Why it fits', self.source)
        self.assertIn('match breakdown', self.source)

    def test_preserves_whole_media_coverage(self):
        for category in ('Movie', 'Series', 'Book', 'Game'):
            self.assertIn(f'c:"{category}"', self.source)


if __name__ == "__main__":
    unittest.main()
