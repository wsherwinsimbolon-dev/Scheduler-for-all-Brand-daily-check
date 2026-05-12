"""
Runner untuk daily check automation.
Scan semua file .py di Daily check All Brand/SGM/ dan jalanin satu per satu.
File yang dimulai dengan 'Locator_' akan di-skip (karena itu POM, bukan test).
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# ============================================================
# KONFIGURASI
# ============================================================

TEST_ROOT = Path("Daily check All Brand") / "SGM"
SKIP_PREFIXES = ("Locator_",)
TEST_TIMEOUT = 300


# ============================================================
# LOGIC
# ============================================================

def find_test_files(root: Path):
    test_files = []
    if not root.exists():
        print(f"❌ Folder tidak ditemukan: {root}")
        return test_files

    for py_file in root.rglob("*.py"):
        if py_file.name.startswith(SKIP_PREFIXES):
            continue
        if py_file.name.startswith("__"):
            continue
        test_files.append(py_file)

    return sorted(test_files)


def run_single_test(test_file: Path):
    start = datetime.now()
    try:
        # Set PYTHONPATH supaya Python bisa nemu Locator_*.py di folder yang sama
        env = os.environ.copy()
        test_folder = str(test_file.parent.absolute())
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{test_folder}{os.pathsep}{existing}" if existing else test_folder

        # PENTING: pakai .absolute() supaya path-nya gak relatif terhadap cwd
        result = subprocess.run(
            [sys.executable, str(test_file.absolute())],
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT,
            cwd=str(test_file.parent.absolute()),
            env=env,
        )
        duration = (datetime.now() - start).total_seconds()
        success = result.returncode == 0
        output = result.stdout + ("\n--- STDERR ---\n" + result.stderr if result.stderr else "")
        return success, output, duration

    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start).total_seconds()
        return False, f"⏱️ TIMEOUT setelah {TEST_TIMEOUT} detik", duration

    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        return False, f"💥 ERROR: {type(e).__name__}: {e}", duration


def main():
    print("=" * 70)
    print(f"🚀 DAILY CHECK AUTOMATION")
    print(f"⏰ Mulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    test_files = find_test_files(TEST_ROOT)
    total = len(test_files)

    if total == 0:
        print(f"⚠️  Tidak ada file test ditemukan di {TEST_ROOT}")
        sys.exit(1)

    print(f"📋 Total {total} test case ditemukan\n")

    passed = []
    failed = []

    for i, test_file in enumerate(test_files, start=1):
        relative_path = test_file.relative_to(TEST_ROOT.parent)
        print(f"\n[{i}/{total}] ▶️  {relative_path}")
        print("-" * 70)

        success, output, duration = run_single_test(test_file)

        if output.strip():
            print(output)

        if success:
            print(f"✅ PASS ({duration:.1f}s)")
            passed.append(str(relative_path))
        else:
            print(f"❌ FAIL ({duration:.1f}s)")
            failed.append(str(relative_path))

    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total      : {total}")
    print(f"✅ PASSED  : {len(passed)}")
    print(f"❌ FAILED  : {len(failed)}")
    print(f"⏰ Selesai : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if failed:
        print("\n❌ Test yang GAGAL:")
        for f in failed:
            print(f"   - {f}")

    print("=" * 70)
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
