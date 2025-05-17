# VRChat Account Manager

VRChat Account Manager allows switching between multiple VRChat SDK accounts on Windows. It backs up and restores the encrypted registry keys as well as the per-project AppData folders. A lightweight SQLite database keeps track of saved accounts and bindings.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The GUI lists Unity projects on the left and stored accounts on the right. Use the toolbar to add or remove accounts, back up a project, or switch the selected project to a different account.

Registry manipulation only works on Windows. On other platforms the project list will be empty.

