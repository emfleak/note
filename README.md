# 📝 note — A Fast Terminal Note-Taking Tool

**note** is a lightweight, terminal-first note-taking app designed for **speed**, **clarity**, and **power**. Whether you're jotting quick tasks or logging structured thoughts, `note` lets you do it all from the command line — instantly.

---

## Features

- Quick inline notes with `note "this is a note"`  
- Multiline notes with your favorite editor (`nano`, `vim`, etc.)
- Fuzzy search picker with `fzf`
- Append to or edit existing notes by number
- Tagging support (`--tags`)
- Delete notes by number, or purge everything with confirmation
- Human-readable JSON storage (~/.notes_db.json)
- Colorized output for readability

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/emfleak/note.git
cd note
```

### 2. Install dependencies

```bash
pip install colorama
```

Install `fzf`:

```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt install fzf
```

### 3. Install the CLI

```bash
chmod +x note.py
mv note.py /usr/local/bin/note  # Or any directory in your PATH
```

## 🧪 Example Usage

### ⚡ Quick notes

```bash
note "Fix broken redirect in Nginx"
```

### Multiline notes

```bash
note add
```

Will launch nano. Add `--tags` for organization:

```bash
note add --tags project journal
```

### List notes

```bash
note list           # Clean view (line number, time, preview)
note list -a        # Full view (includes ID and tags)
```

### Search notes

```bash
note search nginx
```

### Tag notes

```bash
note "Add SSL to API gateway" --tags infra security
note tags           # Show all tags
note tags infra     # Filter by tag
```

### Edit or append to notes

```bash
note append 2 "Add link to bug ticket"
note edit 3
```

### Delete notes

```bash
note del 4
note --delete-all   # Prompts for confirmation
```

---

## Interactive Picker (fzf)

Run `note` with no arguments to launch an interactive fuzzy-searchable picker:

```bash
note
```

- Type to filter notes
- Use arrow keys and Enter to:
  - (v)iew]
  - (e)dit
  - (d)elete
- Supports **multi-select** for bulk deletion
- Colorized and tag-aware

---

## Example Output

```bash
note list -a

1   94d8f0a2   9:05AM Mon, Apr 29 2025   Fix redirect issue        [infra, urgent]
2   b21c3a0e   10:30AM Tue, Apr 30 2025  Finalize meeting agenda   [work, planning]
```

## 📁 Storage

All notes are stored in:

```
~/.notes_db.json
```

This makes it easy to back up, sync, or inspect manually.

---

## Why use `note`?

- Fast and responsive (keyboard-only)
- Cleaner than sticky notes, simpler than Notion
- Cross-platform: macOS, Linux, WSL
- Syncable: just version your `~/.notes_db.json`

---

## Help

```bash
note --help
```

Shows full usage instructions and examples.

---

## License

MIT
