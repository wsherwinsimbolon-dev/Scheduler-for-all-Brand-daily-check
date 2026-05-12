"""
Patcher: Auto-ubah semua file Playwright test yang punya headless=False
supaya bisa auto-detect environment (lokal: headful, CI: headless).
"""

from pathlib import Path

TARGET_FOLDER = Path("Daily check All Brand") / "SGM"
HEADLESS_LINE = 'HEADLESS = os.environ.get("CI", "").lower() == "true"'


def patch_file(file_path: Path) -> bool:
    content = file_path.read_text(encoding="utf-8")

    if "headless=False" not in content:
        return False

    lines = content.split("\n")
    has_import_os = any(line.strip() == "import os" or line.strip().startswith("import os ")
                        for line in lines)
    has_headless_var = any("HEADLESS" in line and "os.environ" in line for line in lines)

    last_import_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            last_import_idx = i

    if last_import_idx == -1:
        last_import_idx = 0

    inserted_lines = []
    if not has_import_os:
        inserted_lines.append("import os")
    if not has_headless_var:
        inserted_lines.append(HEADLESS_LINE)

    if inserted_lines:
        new_lines = lines[:last_import_idx + 1] + inserted_lines + lines[last_import_idx + 1:]
    else:
        new_lines = lines

    new_content = "\n".join(new_lines)
    new_content = new_content.replace("headless=False", "headless=HEADLESS")

    file_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    if not TARGET_FOLDER.exists():
        print(f"❌ Folder gak ada: {TARGET_FOLDER}")
        return

    patched = []
    for py_file in TARGET_FOLDER.rglob("*.py"):
        if patch_file(py_file):
            patched.append(py_file)
            print(f"✅ Patched: {py_file}")

    print("\n" + "=" * 60)
    print(f"📊 Total patched: {len(patched)} files")
    print("=" * 60)


if __name__ == "__main__":
    main()
