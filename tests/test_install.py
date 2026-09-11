"""Exercise installs in temporary Codex homes, including failure recovery."""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.home = self.work / "codex home"
        self.target = self.home / "pets" / "eyjafjalla"
        self.source = self.work / "source bundle"
        shutil.copytree(ROOT / "pets" / "eyjafjalla", self.source)
        self.env = dict(os.environ, CODEX_HOME=str(self.home))

    def run_install(self, *args, ok=True):
        result = subprocess.run(
            ["bash", str(ROOT / "install.sh"), *args],
            env=self.env, text=True, capture_output=True,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def local(self, ok=True):
        return self.run_install("--source", str(self.source), ok=ok)

    def backups(self):
        return list((self.home / "pet-backups").glob("eyjafjalla.*/pet"))

    def assert_clean(self):
        self.assertEqual(list((self.home / "pets").glob(".eyjafjalla-*")), [])

    def change_source(self):
        with (self.source / "pet.json").open("a") as stream:
            stream.write("\n")
        (self.source / "checksums.sha256").write_text("".join(
            f"{hashlib.sha256((self.source / name).read_bytes()).hexdigest()}  {name}\n"
            for name in ("pet.json", "spritesheet.webp")
        ))

    def mock(self, name, body):
        directory = self.work / "bin"
        directory.mkdir(exist_ok=True)
        script = directory / name
        script.write_text("#!/bin/bash\nset -eu\n" + body)
        script.chmod(0o755)
        self.env["PATH"] = str(directory) + os.pathsep + os.environ["PATH"]

    def test_fresh_install_and_repeat_preserves_extra_files(self):
        self.local()
        self.assertEqual((self.target / "pet.json").read_bytes(), (self.source / "pet.json").read_bytes())
        (self.target / "personal.txt").write_text("keep me")
        result = self.local()
        self.assertIn("already up to date", result.stdout)
        self.assertTrue((self.target / "personal.txt").exists())
        self.assertEqual(self.backups(), [])
        self.assert_clean()

    def test_upgrade_preserves_entire_previous_directory(self):
        self.local()
        old = (self.target / "pet.json").read_bytes()
        (self.target / "personal.txt").write_text("keep me")
        self.change_source()
        self.local()
        self.assertEqual(len(self.backups()), 1)
        self.assertEqual((self.backups()[0] / "pet.json").read_bytes(), old)
        self.assertEqual((self.backups()[0] / "personal.txt").read_text(), "keep me")
        self.assertEqual((self.target / "pet.json").read_bytes(), (self.source / "pet.json").read_bytes())
        self.assert_clean()

    def test_corrupt_download_keeps_existing_pet(self):
        self.local()
        old = (self.target / "spritesheet.webp").read_bytes()
        (self.source / "spritesheet.webp").write_bytes(b"broken")
        self.assertIn("Checksum mismatch", self.local(ok=False).stderr)
        self.assertEqual((self.target / "spritesheet.webp").read_bytes(), old)
        self.assertEqual(self.backups(), [])
        self.assert_clean()

    def test_missing_file_leaves_no_partial_install(self):
        (self.source / "pet.json").unlink()
        self.local(ok=False)
        self.assertFalse(self.target.exists())
        self.assert_clean()

    def test_manifest_cannot_redirect_checks(self):
        (self.source / "checksums.sha256").write_text("a" * 64 + "  ../../pet.json\n")
        self.assertIn("Invalid checksum entry", self.local(ok=False).stderr)
        self.assertFalse(self.target.exists())
        self.assert_clean()

    def test_uninstall_is_recoverable_and_repeatable(self):
        self.local()
        self.run_install("--uninstall")
        self.assertFalse(self.target.exists())
        self.assertTrue((self.backups()[0] / "spritesheet.webp").exists())
        self.run_install("--uninstall")
        self.assertEqual(len(self.backups()), 1)
        self.assert_clean()

    def test_symlink_destination_is_untouched(self):
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.source, target_is_directory=True)
        self.assertIn("symlink", self.local(ok=False).stderr)
        self.assertTrue(self.target.is_symlink())
        self.assert_clean()

    def test_concurrent_lock_is_respected(self):
        lock = self.target.parent / ".eyjafjalla-install.lock"
        lock.mkdir(parents=True)
        self.assertIn("Another install", self.local(ok=False).stderr)
        self.assertTrue(lock.is_dir())
        self.assertFalse(self.target.exists())

    def test_invalid_arguments(self):
        for args in [("--oops",), ("--source",), ("--ref",), ("--source", str(self.source), "--ref", "main"), ("--uninstall", "--ref", "main")]:
            with self.subTest(args=args):
                self.run_install(*args, ok=False)
        self.assertFalse(self.target.exists())

    def test_remote_ref_and_download_failure(self):
        self.env["FIXTURE_BUNDLE"] = str(self.source)
        self.env["URL_LOG"] = str(self.work / "urls")
        self.mock("curl", '''url=''
dest=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    https://*) url=$1; shift ;;
    -o) dest=$2; shift 2 ;;
    *) shift ;;
  esac
done
printf '%s\\n' "$url" >> "$URL_LOG"
cp "$FIXTURE_BUNDLE/${url##*/}" "$dest"
''')
        self.run_install("--ref", "v1.0.0")
        self.assertIn("/v1.0.0/pets/eyjafjalla/", (self.work / "urls").read_text())
        old = (self.target / "pet.json").read_bytes()
        self.mock("curl", "exit 22\n")
        self.run_install(ok=False)
        self.assertEqual((self.target / "pet.json").read_bytes(), old)
        self.assertEqual(self.backups(), [])
        self.assert_clean()

    def test_failed_replacement_rolls_back(self):
        self.local()
        old = (self.target / "pet.json").read_bytes()
        self.change_source()
        self.env["REAL_MV"] = shutil.which("mv")
        self.mock("mv", '''case "$1" in
  */.eyjafjalla-stage.*) exit 1 ;;
esac
exec "$REAL_MV" "$@"
''')
        self.local(ok=False)
        self.assertEqual((self.target / "pet.json").read_bytes(), old)
        self.assert_clean()


if __name__ == "__main__":
    unittest.main()
