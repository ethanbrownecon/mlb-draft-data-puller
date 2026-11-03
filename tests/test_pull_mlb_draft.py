import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from pull_mlb_draft import fetch_draft, main


def api_response():
    return {
        "drafts": {
            "rounds": [
                {
                    "round": "1",
                    "picks": [
                        {"pickNumber": 1, "person": {"fullName": "Sample Player"}}
                    ],
                },
                {"round": "2", "picks": [{"pickNumber": 2}]},
            ]
        }
    }


class FetchDraftTests(unittest.TestCase):
    def test_normalizes_api_picks_and_adds_year_and_pick(self):
        session = MagicMock()
        session.get.return_value.json.return_value = api_response()

        result = fetch_draft(2025, session)

        self.assertEqual(result["year"].tolist(), [2025, 2025])
        self.assertEqual(result["pick"].tolist(), [1, 2])
        self.assertEqual(result["round"].tolist(), ["1", "2"])
        session.get.assert_called_once_with(
            "https://statsapi.mlb.com/api/v1/draft/2025",
            timeout=30,
        )
        session.get.return_value.raise_for_status.assert_called_once()

    def test_rejects_unexpected_api_response(self):
        session = MagicMock()
        session.get.return_value.json.return_value = {"drafts": {}}

        with self.assertRaisesRegex(ValueError, "no draft rounds"):
            fetch_draft(2025, session)


class CommandLineTests(unittest.TestCase):
    @patch("pull_mlb_draft.requests.Session")
    def test_writes_yearly_and_combined_csvs(self, session_factory):
        session = MagicMock()
        session_factory.return_value.__enter__.return_value = session
        session.get.return_value.json.return_value = api_response()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = main(
                [
                    "--start-year",
                    "2024",
                    "--end-year",
                    "2025",
                    "--output-dir",
                    temp_dir,
                ]
            )
            output_dir = Path(temp_dir)

            self.assertEqual(result, 0)
            self.assertTrue((output_dir / "draft_2024.csv").is_file())
            self.assertTrue((output_dir / "draft_2025.csv").is_file())
            combined = pd.read_csv(output_dir / "draft_2024_2025.csv")
            self.assertEqual(combined["year"].tolist(), [2024, 2024, 2025, 2025])


if __name__ == "__main__":
    unittest.main()
