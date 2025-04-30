#!/usr/bin/env python3
import sys, json, os, subprocess, tempfile
from datetime import datetime
from uuid import uuid4
from colorama import Fore, Style, init

init(autoreset=True)

DB_PATH = os.path.expanduser("~/.notes_db.json")

def pretty_time(timestring):
    dt = datetime.fromisoformat(timestring)
    return dt.strftime("%-I:%M%p %a, %b %d %Y")

def print_help():
    help_text = """
Note - A fast terminal note-taking tool

Usage:
  note "your note text"           Add a new note
  note add                        Add a new multiline note using your editor
  note list                       List notes (line number, timestamp, snippet)
  note list -a                    List notes with full ID and extra info
  note del <number>               Delete a note by line number
  note append <number> "text"     Append text to an existing note
  note edit <number>              Edit a note in your default text editor
  note search <keyword>           Search notes for a keyword
  note --delete-all               Delete ALL notes (with confirmation)
  note                            Launch interactive picker (with fzf)

Options:
  -a                              Show all info (IDs) in list mode
  --delete-all                    Delete all notes after confirmation
  $EDITOR                         Use your preferred editor for editing notes (defaults to nano)

Examples:
  note "Buy milk and eggs"
  note list
  note del 2
  note append 1 "Remember to call John"
  note edit 3
  note search project
  note --delete-all
"""
    print(help_text)

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)

def add_note(text):
    db = load_db()
    note_id = str(uuid4())[:8]
    db[note_id] = {
        "timestamp": datetime.now().isoformat(),
        "content": text
    }
    save_db(db)
    print(f"Note saved with ID {note_id}")

def add_note_with_editor():
    editor = os.environ.get("EDITOR", "nano")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    subprocess.call([editor, tmp_path])

    with open(tmp_path, 'r') as tmp:
        content = tmp.read()

    os.unlink(tmp_path)

    if content.strip():
        add_note(content)
    else:
        print("Empty note discarded.")

def list_notes(all_info=False):
    db = load_db()
    if not db:
        print("No notes yet.")
        return
    for idx, (nid, note) in enumerate(db.items(), start=1):
        dt = pretty_time(note['timestamp'])
        preview = note['content'][:100].replace('\n', ' ')
        if all_info:
            print(
                f"{Fore.GREEN}{idx}{Style.RESET_ALL}\t"
                f"{Fore.BLUE}{nid}{Style.RESET_ALL}\t"
                f"{Fore.LIGHTBLACK_EX}{dt}{Style.RESET_ALL}\t"
                f"{preview}"
            )
        else:
            print(
                f"{Fore.GREEN}{idx}{Style.RESET_ALL}\t"
                f"{Fore.LIGHTBLACK_EX}{dt}{Style.RESET_ALL}\t"
                f"{preview}"
            )

def delete_note(line_number):
    db = load_db()
    keys = list(db.keys())
    if 1 <= line_number <= len(keys):
        nid = keys[line_number - 1]
        del db[nid]
        save_db(db)
        print(f"Deleted note {nid}")
    else:
        print("Invalid note number.")

def delete_all_notes():
    db = load_db()
    if not db:
        print("No notes to delete.")
        return
    confirm = input("Are you sure you want to delete ALL notes? (y/n) > ").strip().lower()
    if confirm == 'y':
        save_db({})
        print("All notes deleted.")
    else:
        print("Cancelled.")

def append_note(line_number, text):
    db = load_db()
    keys = list(db.keys())
    if 1 <= line_number <= len(keys):
        nid = keys[line_number - 1]
        db[nid]['content'] += "\n" + text
        save_db(db)
        print(f"Appended to note {nid}")
    else:
        print("Invalid note number.")

def edit_note(line_number):
    db = load_db()
    keys = list(db.keys())
    if not (1 <= line_number <= len(keys)):
        print("Invalid note number.")
        return

    nid = keys[line_number - 1]
    content = db[nid]['content']

    editor = os.environ.get("EDITOR", "nano")  # use $EDITOR if set, fallback to nano

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        tmp_path = tmp.name

    subprocess.call([editor, tmp_path])

    with open(tmp_path, 'r') as tmp:
        updated_content = tmp.read()

    os.unlink(tmp_path)

    if updated_content.strip() != content.strip():
        db[nid]['content'] = updated_content
        save_db(db)
        print("Note updated.")
    else:
        print("No changes made.")

def edit_note_by_id(nid):
    db = load_db()
    content = db[nid]['content']

    editor = os.environ.get("EDITOR", "nano")
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        tmp_path = tmp.name

    subprocess.call([editor, tmp_path])

    with open(tmp_path, 'r') as tmp:
        updated_content = tmp.read()

    os.unlink(tmp_path)

    if updated_content.strip() != content.strip():
        db[nid]['content'] = updated_content
        save_db(db)
        print("Note updated.")
    else:
        print("No changes made.")

def search_notes(keyword):
    db = load_db()
    keyword = keyword.lower()
    found = False
    for idx, (nid, note) in enumerate(db.items(), start=1):
        if keyword in note['content'].lower():
            dt = note['timestamp']
            preview = note['content'][:100].replace('\n', ' ')
            print(f"{idx}\t{nid}\t{dt}\t{preview}")
            found = True
    if not found:
        print(f"No notes found containing '{keyword}'.")

def pick_with_fzf():
    db = load_db()
    if not db:
        print("No notes to pick.")
        return

    lines = []
    keys = list(db.keys())

    for idx, (nid, note) in enumerate(db.items(), start=1):
        dt = pretty_time(note['timestamp'])
        preview = note['content'][:100].replace('\n', ' ')
        line = f"{idx}\t{nid}\t{dt}\t{preview}"
        lines.append(line)

    try:
        fzf = subprocess.run(
            ["fzf", "--multi", "--prompt=Select note(s): "],
            input="\n".join(lines),
            text=True,
            capture_output=True
        )
        if fzf.returncode != 0 or not fzf.stdout.strip():
            return

        selected_lines = fzf.stdout.strip().splitlines()
        selected_idxs = [int(line.split("\t")[0]) for line in selected_lines]
        selected_ids = [keys[idx - 1] for idx in selected_idxs]

        if len(selected_ids) == 1:
            nid = selected_ids[0]
            action = input("Action? (v)iew (e)dit (a)ppend (d)elete > ").strip().lower()
            if action == "v":
                print("\n=== Note ===")
                print(db[nid]['content'])
            elif action == "d":
                confirm = input(f"Delete note {nid}? (y/n) > ")
                if confirm.lower() == 'y':
                    del db[nid]
                    save_db(db)
                    print("Note deleted.")
            elif action == "a":
                text = input("Append text: ")
                db[nid]['content'] += "\n" + text
                save_db(db)
                print("Note updated.")
            elif action == "e":
                edit_note_by_id(nid)
            else:
                print("Unknown action.")
        else:
            print("Selected notes:")
            for nid in selected_ids:
                print(f"- {nid}")
            confirm = input("Delete all selected notes? (y/n) > ").strip().lower()
            if confirm == 'y':
                for nid in selected_ids:
                    del db[nid]
                save_db(db)
                print(f"Deleted {len(selected_ids)} notes.")
            else:
                print("Cancelled.")

    except Exception as e:
        print(f"Error using fzf: {e}")

def main():
    args = sys.argv[1:]
    if not args:
        pick_with_fzf()
        return
    if args[0] in ["-h", "--help", "help"]:
        print_help()
    elif args[0] == "add" and len(args) == 1:
        add_note_with_editor()
    elif args[0] == "list":
        if len(args) > 1 and args[1] == "-a":
            list_notes(all_info=True)
        else:
            list_notes(all_info=False)
    elif args[0] == "--delete-all":
        delete_all_notes()
    elif args[0] == "del" and len(args) == 2:
        try:
            line_number = int(args[1])
            delete_note(line_number)
        except ValueError:
            print("Please provide a valid number.")
    elif args[0] == "append" and len(args) >= 3:
        try:
            line_number = int(args[1])
            append_note(line_number, ' '.join(args[2:]))
        except ValueError:
            print("Please provide a valid number.")
    elif args[0] == "edit" and len(args) == 2:
        try:
            line_number = int(args[1])
            edit_note(line_number)
        except ValueError:
            print("Please provide a valid number.")
    elif args[0] == "search" and len(args) >= 2:
        search_notes(' '.join(args[1:]))
    else:
        add_note(' '.join(args))

if __name__ == "__main__":
    main()
