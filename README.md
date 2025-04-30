# note — A Terminal Note-Taking Tool

**note** is a simple, fast, and keyboard-friendly CLI tool for capturing, browsing, editing, and managing personal notes directly from your terminal.

Designed for speed and minimalism, it supports both **quick one-liner notes** and full multiline notes using your favorite editor.

---

## Features

- ✅ One-liner notes right from the command line
- 📝 Full multiline notes in `$EDITOR` (`nano`, `vim`, etc.)
- 🔍 Fuzzy search with `fzf` picker
- 🧠 Append, edit, and delete notes easily
- 📋 List notes with timestamps and previews
- 📦 JSON-based storage (`~/.notes_db.json`)
- 🛠 Works entirely offline and cross-platform

---

## 📦 Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/note.git
   cd note
   ```

2. Install dependencies:

   ```bash
   pip install colorama
   ```

   Also install `fzf`:

   ```bash
   # macOS
   brew install fzf

   # Debian/Ubuntu
   sudo apt install fzf
   ```

3. Make it executable and move it into your PATH:

   ```bash
   chmod +x note.py
   mv note.py /usr/local/bin/note  # or somewhere in your PATH
   ```

4. (Optional) Set your preferred editor:

   ```bash
   export EDITOR=nvim   # or vim, code, micro, etc.
   ```

---

## 🧪 Usage

### ✅ Quick notes

```bash
note "Fix Nginx redirect issue"
```

Adds a one-liner note instantly.

---

### 📋 List notes

```bash
note list           # Basic listing (line number, time, preview)
note list -a        # Full info (includes internal ID)
```

---

### 📝 Add multiline note

```bash
note add
```

Opens your `$EDITOR` to create a longer note.

---

### ➕ Append to a note

```bash
note append 2 "Add link to bug report"
```

---

### 🛠 Edit a note

```bash
note edit 3
```

Opens the selected note in your editor for full editing.

---

### ❌ Delete a note

```bash
note del 4
```

---

### 💣 Delete ALL notes (with confirmation)

```bash
note --delete-all
```

---

### 🔍 Search notes

```bash
note search nginx
```

Case-insensitive search across all notes.

---

### 🎯 Use interactive picker

```bash
note
```

- Uses `fzf` to let you:
  - Select one or more notes
  - View, append, edit, or delete them
  - Multi-select for bulk deletion

---

## 📁 Where are notes stored?

All notes are saved in:

```
~/.notes_db.json
```

This makes it easy to back up, version, or sync manually.

---

## ✅ Example Output

```bash
note list

1   9:05AM Mon, Apr 29 2025   Fix redirect bug in Nginx config
2   2:45PM Tue, Apr 30 2025   Talk with ops about service restart
```

---

## 🙌 Why Use This?

- Works everywhere (Linux, macOS, WSL)
- Instant launch — perfect for muscle-memory workflows
- No cloud, no database, just your words
- Fzf-powered navigation is lightning-fast

---

## License

MIT

---

## Contributions

Ideas are welcome.
