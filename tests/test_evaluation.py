"""Automated tests for OJW lexical evaluation harness."""

import tempfile
import unittest
from pathlib import Path

from kawi_tts.evaluation.evaluate_ojw import evaluate_ojw, load_ojw_dataset


class TestOJWEvaluation(unittest.TestCase):
    """Test suite for OJW lexical coverage evaluation."""

    def test_load_ojw_dataset_real_counts(self):
        """Verifies parsing and deduplication logic on the actual downloaded wn-kaw.tab."""
        raw_path = Path("data/raw/wn-kaw.tab")
        if not raw_path.exists():
            self.skipTest("data/raw/wn-kaw.tab not found")

        stats, unique_forms = load_ojw_dataset(raw_path)
        self.assertEqual(stats.total_raw_lines, 5020)
        self.assertEqual(stats.data_rows, 5019)
        self.assertEqual(stats.header_lines, 1)
        self.assertEqual(stats.unique_synsets, 2032)
        self.assertEqual(stats.unique_lemmas, 3632)
        self.assertEqual(stats.unique_variants, 569)
        self.assertEqual(stats.unique_lexical_forms, 4192)
        self.assertEqual(len(unique_forms), 4192)

    def test_evaluate_ojw_mock_dataset(self):
        """Verifies evaluation metrics computation on a controlled TSV fixture."""
        mock_tsv = (
            "# Test Header\n"
            "00000001-n\tkaw:lemma\tsĕkar\tmabrĕsih\n"
            "00000002-n\tkaw:lemma\tbhaṭāra\n"
            "00000003-n\tkaw:lemma\ttīrthâṅga\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tsv_path = Path(tmpdir) / "mock.tab"
            json_path = Path(tmpdir) / "report.json"
            tsv_path.write_text(mock_tsv, encoding="utf-8")

            report = evaluate_ojw(file_path=tsv_path, output_json=json_path)

            self.assertEqual(report.total_evaluated, 4)  # sĕkar, mabrĕsih, bhaṭāra, tīrthâṅga
            self.assertEqual(report.runtime_exceptions_count, 0)
            self.assertEqual(report.forms_with_unsupported_chars, 1)  # tīrthâṅga has 'â'
            self.assertEqual(report.fully_supported_count, 3)
            self.assertEqual(report.fully_supported_pct, 75.0)
            self.assertTrue(json_path.exists())

    def test_ojw_high_throughput_coverage_rate(self):
        """Verifies that full OJW evaluation achieves >= 99.5% representation coverage."""
        raw_path = Path("data/raw/wn-kaw.tab")
        if not raw_path.exists():
            self.skipTest("data/raw/wn-kaw.tab not found")

        json_path = Path("data/processed/ojw_coverage_report.json")
        report = evaluate_ojw(file_path=raw_path, output_json=json_path)

        self.assertEqual(report.total_evaluated, 4192)
        self.assertEqual(report.runtime_exceptions_count, 0)
        self.assertGreaterEqual(report.fully_supported_pct, 99.5)
        self.assertEqual(report.forms_with_unsupported_chars, 4)
        self.assertEqual(
            set(report.unsupported_char_frequencies.keys()),
            {"î", "ṃ", "â", "ḥ"},
        )


if __name__ == "__main__":
    unittest.main()
