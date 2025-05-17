# VRChat Account Manager

VRChat Account Manager provides utilities to backup, restore and switch VRChat SDK credentials across multiple Unity projects.  Registry and AppData entries are handled using Python and PySide6 offers a simple GUI.

## Setup

Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

Run the GUI application:

```bash
python main.py
```

The program lists detected Unity projects and locally stored accounts.  Right click a project to perform a backup.  Account switching will update the Windows registry for that project.

### Packaging

On Windows you can build a portable executable using PyInstaller:

```cmd
pyinstaller --onefile --windowed main.py -n VRChatAcctMgr
```

The resulting `dist/VRChatAcctMgr.exe` can be distributed as a single file.

**Warning**: modifying the Windows registry may affect your VRChat installation.  Always keep backups of registry values and AppData directories.

