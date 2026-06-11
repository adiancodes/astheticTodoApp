"""
app.py — Multi-page Productivity App (Google Keep-inspired)
------------------------------------------------------------
Two pages:
  /        → Todo list  (index.html)
  /notes   → Notes      (keep.html)

No database — everything lives in plain Python lists.
"""

import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# ---------------------------------------------------------------------------
# IN-MEMORY DATA STORES
# ---------------------------------------------------------------------------

# Each todo looks like: { "id": 1, "text": "Buy milk", "done": False }
todos = []
todo_next_id = 1

# ---------------------------------------------------------------------------
# MOTIVATIONAL QUOTES
# ---------------------------------------------------------------------------
# random.choice() picks one of these every time the todo page loads.
# Add or remove quotes freely — just keep the same (text, author) tuple format.

QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Focus on being productive instead of busy.", "Tim Ferriss"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Small daily improvements over time lead to stunning results.", "Robin Sharma"),
    ("Discipline is choosing between what you want now and what you want most.", "Abraham Lincoln"),
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("It's not about having time. It's about making time.", "Unknown"),
    ("Done is better than perfect.", "Sheryl Sandberg"),
    ("Your future is created by what you do today, not tomorrow.", "Robert Kiyosaki"),
    ("Energy and persistence conquer all things.", "Benjamin Franklin"),
]

# Each note looks like: { "id": 1, "body": "Call dentist tomorrow", "color": "#ffffff" }
# color is the hex code chosen in the palette — defaults to white.
notes = []
note_next_id = 1


# ---------------------------------------------------------------------------
# TODO ROUTES  →  "/"
# ---------------------------------------------------------------------------

@app.route("/")
def todo_page():
    """
    Show the todo list.

    PROGRESS CALCULATION:
      completed = number of todos where done is True
      total     = total number of todos
      pct       = integer percentage (0-100), safe when total is 0

    RANDOM QUOTE:
      random.choice(QUOTES) returns a different (text, author) tuple
      on every page load or refresh.
    """
    completed = sum(1 for t in todos if t["done"])   # count True entries
    total     = len(todos)
    pct       = int((completed / total) * 100) if total > 0 else 0

    quote_text, quote_author = random.choice(QUOTES)

    return render_template(
        "index.html",
        todos=todos,
        active="todo",
        completed=completed,
        total=total,
        pct=pct,
        quote_text=quote_text,
        quote_author=quote_author,
    )


@app.route("/todo/add", methods=["POST"])
def add_todo():
    """Add a new todo item."""
    global todo_next_id
    text = request.form.get("todo_text", "").strip()
    if text:
        todos.append({"id": todo_next_id, "text": text, "done": False})
        todo_next_id += 1
    return redirect(url_for("todo_page"))


@app.route("/todo/toggle/<int:todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    """Flip a todo's done/undone state."""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            break
    return redirect(url_for("todo_page"))


@app.route("/todo/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    """Remove a todo from the list."""
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return redirect(url_for("todo_page"))


# ---------------------------------------------------------------------------
# NOTES ROUTES  →  "/notes"
# ---------------------------------------------------------------------------

@app.route("/notes")
def notes_page():
    """Show the notes grid."""
    return render_template("keep.html", notes=notes, active="notes")


@app.route("/notes/add", methods=["POST"])
def add_note():
    """Add a new note (text + chosen background color)."""
    global note_next_id
    body = request.form.get("note_body", "").strip()

    # The hidden input 'note_color' carries the hex value chosen in the palette.
    # If nothing was chosen (or the field is missing), we fall back to white.
    color = request.form.get("note_color", "#ffffff").strip() or "#ffffff"

    if body:
        notes.append({"id": note_next_id, "body": body, "color": color})
        note_next_id += 1
    return redirect(url_for("notes_page"))


@app.route("/notes/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    """Delete a note."""
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return redirect(url_for("notes_page"))


# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
