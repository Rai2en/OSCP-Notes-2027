from pathlib import Path
import tempfile
import unittest

from scripts.check_docs import check_documents, document_anchors
from scripts.new_session import ROOT, TEMPLATES, create_session


class NotebookTests(unittest.TestCase):
    def test_pentest_mode_uses_client_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = create_session(Path(tmp) / "assessment", mode="pentest")
            self.assertTrue((dest / "client-report.md").is_file())
            self.assertTrue((dest / "engagement.md").is_file())
            self.assertFalse((dest / "report.md").exists())
            self.assertFalse((dest / "progress.md").exists())

    def test_unknown_mode_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "assessment"
            with self.assertRaises(ValueError):
                create_session(dest, mode="unknown")
            self.assertFalse(dest.exists())

    def test_creates_templates_and_evidence_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = create_session(Path(tmp) / "laboratoire privé")
            for name in TEMPLATES:
                self.assertEqual((dest / name).read_bytes(), (ROOT / "templates" / name).read_bytes())
            for name in ("scans", "evidence", "files", "notes"):
                self.assertTrue((dest / name).is_dir())

    def test_refuses_to_overwrite_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = create_session(Path(tmp) / "lab")
            note = dest / "machine.md"
            note.write_text("My evidence", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                create_session(dest)
            self.assertEqual(note.read_text(encoding="utf-8"), "My evidence")

    def test_refuses_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "file"
            dest.touch()
            with self.assertRaises(FileExistsError):
                create_session(dest)

    def test_refuses_repository_destination(self):
        with self.assertRaises(ValueError):
            create_session(ROOT / "private-test-session")


class DocumentationTests(unittest.TestCase):
    def test_missing_local_link_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[Missing](docs/missing.md#section)", encoding="utf-8")
            self.assertEqual(len(check_documents(root)), 1)

    def test_fences_inline_code_and_external_urls_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "```sh\n[fake](no.md)\n```\n~~~\n[fake](no2.md)\n~~~\n"
                "`[fake](no3.md)`\n[web](https://example.org/a)\n## here\n[section](#here)\n", encoding="utf-8")
            self.assertEqual(check_documents(root), [])

    def test_relative_encoded_and_angle_bracket_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "a file.md").write_text("# heading\n[Home](../README.md)", encoding="utf-8")
            (root / "README.md").write_text(
                "[one](docs/a%20file.md#heading)\n[two](<docs/a file.md>)", encoding="utf-8")
            self.assertEqual(check_documents(root), [])

    def test_link_outside_repository_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[outside](../outside.md)", encoding="utf-8")
            self.assertIn("escapes repository", check_documents(root)[0])

    def test_missing_fragment_detected_in_existing_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Present\n[bad](#absent)", encoding="utf-8")
            self.assertIn("missing fragment", check_documents(root)[0])

    def test_heading_and_explicit_anchor_resolution(self):
        anchors = document_anchors(
            '# Use `id` & scope\n## Use `id` & scope\n'
            '<a id="legacy-bookmark"></a>\n```text\n# fake\n```\n'
        )
        self.assertEqual(anchors, {"use-id--scope", "use-id--scope-1", "legacy-bookmark"})

    def test_moved_file_fragment_is_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "reference.md").write_text('# SMB\n## SMB\n', encoding="utf-8")
            (root / "README.md").write_text('[moved](docs/reference.md#smb-1)', encoding="utf-8")
            self.assertEqual(check_documents(root), [])


if __name__ == "__main__":
    unittest.main()
