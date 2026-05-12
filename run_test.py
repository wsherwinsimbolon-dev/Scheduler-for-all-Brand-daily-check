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

# Folder root tempat semua test berada (relatif terhadap run_test.py)
TEST_ROOT = Path("Daily check All Brand") / "SGM"

# Prefix nama file yang harus di-SKIP (bukan test)
SKIP_PREFIXES = ("Locator_",)

# Timeout per test dalam detik (default 5 menit per script)
TEST_TIMEOUT = 300


# ============================================================
# LOGIC
# ============================================================

def find_test_files(root: Path):
    """Cari semua file .py yang merupakan test case (bukan locator)."""
    test_files = []
    if not root.exists():
        print(f"❌ Folder tidak ditemukan: {root}")
        return test_files

    for py_file in root.rglob("*.py"):
        # Skip file yang awalannya ada di SKIP_PREFIXES
        if py_file.name.startswith(SKIP_PREFIXES):
            continue
        # Skip __init__.py, __pycache__, dll
        if py_file.name.startswith("__"):
            continue
        test_files.append(py_file)

    return sorted(test_files)


def run_single_test(test_file: Path):
    """Jalanin 1 file test, return (success, output, duration_seconds)."""
    start = datetime.now()
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT,
            # Jalankan dari folder script-nya supaya import lokal (Locator_*.py) tetap ketemu
            cwd=str(test_file.parent),
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

        # Print output dari script
        if output.strip():
            print(output)

        if success:
            print(f"✅ PASS ({duration:.1f}s)")
            passed.append(str(relative_path))
        else:
            print(f"❌ FAIL ({duration:.1f}s)")
            failed.append(str(relative_path))

    # ============================================================
    # SUMMARY
    # ============================================================
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

    # Exit code: 0 kalau semua pass, 1 kalau ada yang gagal
    # GitHub Actions baca exit code ini untuk nentuin job status
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
