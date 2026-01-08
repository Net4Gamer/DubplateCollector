import sqlite3
import os

DB_PATH = "dubplates.db"   # change path if needed


# -----------------------------------
# Database initialization
# -----------------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            title TEXT NOT NULL,
            filetype TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def track_exists(conn, artist, title):
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM tracks WHERE artist = ? AND title = ?",
        (artist, title)
    )
    return cur.fetchone() is not None


# -----------------------------------
# Add track
# -----------------------------------

def add_track(conn, artist=None, title=None, filetype=None):
    print("\n=== Add Track (0 — Back) ===")

    if artist is None:
        artist = input("Artist (can be empty): ").strip()
        if artist == "0":
            return

    if title is None:
        title = input("Title: ").strip()
        if title == "0":
            return

    if filetype is None:
        while True:
            filetype = input("Format (mp3/flac/wav/aiff): ").strip().lower()
            if filetype == "0":
                return
            if filetype in ["mp3", "flac", "wav", "aiff"]:
                break
            print("Invalid format.")

    if track_exists(conn, artist, title):
        print(f"⚠ Duplicate: {artist} – {title}")
        return

    conn.execute(
        "INSERT INTO tracks (artist, title, filetype) VALUES (?, ?, ?)",
        (artist, title, filetype)
    )
    conn.commit()

    print(f"✓ Added: {artist} – {title} [{filetype.upper()}]")


# -----------------------------------
# Delete track
# -----------------------------------

def delete_track(conn):
    print("\n=== Delete Track (0 — Back) ===")

    artist = input("Artist (can be empty): ").strip()
    if artist == "0":
        return

    title = input("Title: ").strip()
    if title == "0":
        return

    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tracks WHERE artist = ? AND title = ?",
        (artist, title)
    )
    conn.commit()

    if cur.rowcount > 0:
        print("✓ Track deleted.")
    else:
        print("⚠ Track not found.")


# -----------------------------------
# Search
# -----------------------------------

def search_tracks(conn):
    print("\n=== Search Tracks (0 — Back) ===")

    query = input("Search query: ").strip()
    if query == "0":
        return

    query_lower = query.lower()

    cur = conn.cursor()
    cur.execute("""
        SELECT artist, title, filetype FROM tracks
        WHERE LOWER(artist) LIKE ? OR LOWER(title) LIKE ?
        ORDER BY artist, title
    """, (f"%{query_lower}%", f"%{query_lower}%"))

    rows = cur.fetchall()

    if not rows:
        print("No results found.")
        return

    print(f"\nFound {len(rows)} tracks:\n")
    for artist, title, filetype in rows:
        if artist:
            print(f"{artist} – {title} [{filetype.upper()}]")
        else:
            print(f"{title} [{filetype.upper()}]")


# -----------------------------------
# Export
# -----------------------------------

def export_txt(conn):
    print("\n=== Export ===")

    filename = "export.txt"
    rows = conn.execute(
        "SELECT artist, title, filetype FROM tracks ORDER BY artist, title"
    ).fetchall()

    with open(filename, "w", encoding="utf-8") as f:
        for artist, title, filetype in rows:
            if artist:
                f.write(f"{artist} – {title} [{filetype.upper()}]\n")
            else:
                f.write(f"{title} [{filetype.upper()}]\n")

    print(f"✓ Export saved to {filename}")


# -----------------------------------
# Import: Format 1
# Artist - Title.ext
# -----------------------------------

def import_format_simple(conn, lines):
    print("\n📥 Import: Artist - Title.Filetype")

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if "." not in line:
            print(f"⚠ Skipped (no file extension): {line}")
            continue

        name_part, ext = line.rsplit(".", 1)
        ext = ext.lower()

        if ext not in ["mp3", "wav", "flac", "aiff"]:
            print(f"⚠ Unknown format: {line}")
            continue

        if " - " in name_part:
            artist, title = name_part.split(" - ", 1)
            artist = artist.strip()
            title = title.strip()
        else:
            artist = ""
            title = name_part.strip()

        add_track(conn, artist, title, ext)


# -----------------------------------
# Import: Format 2 (Export Format)
# Artist – Title [AIFF]
# -----------------------------------

def import_format_export(conn, lines):
    print("\n📥 Import: DubplateCollector Export Format")

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if "[" not in line or "]" not in line:
            print(f"⚠ Skipped: {line}")
            continue

        try:
            filetype = line[line.rfind("[")+1 : line.rfind("]")].lower()
        except:
            print(f"⚠ Format parse error: {line}")
            continue

        if filetype not in ["mp3", "wav", "flac", "aiff"]:
            print(f"⚠ Unknown format '{filetype}': {line}")
            continue

        main = line[:line.rfind("[")].strip()

        if "–" in main:
            artist, title = main.split("–", 1)
            artist = artist.strip()
            title = title.strip()
        else:
            artist = ""
            title = main.strip()

        add_track(conn, artist, title, filetype)


# -----------------------------------
# Import from TXT
# -----------------------------------

def import_from_txt(conn):
    print("\n=== Import from TXT (0 — Back) ===")

    print("1 — Artist - Title.Filetype")
    print("2 — DubplateCollector Export Format")

    choice = input("> ").strip()
    if choice == "0":
        return

    if choice not in ["1", "2"]:
        print("Invalid option.")
        return

    path = input("Enter path to TXT file: ").strip()
    if path == "0":
        return

    if not os.path.exists(path):
        print("File not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if choice == "1":
        import_format_simple(conn, lines)
    elif choice == "2":
        import_format_export(conn, lines)


# -----------------------------------
# Main menu
# -----------------------------------

def main():
    conn = init_db()

    while True:
        print("\n=== Main Menu ===")
        print("1 — Add Track")
        print("2 — Delete Track")
        print("3 — Search")
        print("4 — Export to TXT")
        print("5 — Import from TXT")
        print("0 — Exit")

        choice = input("> ").strip()

        if choice == "1":
            add_track(conn)
        elif choice == "2":
            delete_track(conn)
        elif choice == "3":
            search_tracks(conn)
        elif choice == "4":
            export_txt(conn)
        elif choice == "5":
            import_from_txt(conn)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
