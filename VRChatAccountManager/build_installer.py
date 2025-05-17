import PyInstaller.__main__
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    main_script = project_root / "main.py"
    PyInstaller.__main__.run([
        str(main_script),
        "--onefile",
        "--noconsole",
        "--name",
        "VRChatAcctMgr",
    ])
