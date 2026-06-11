"""
app.py — Multi-page Productivity App (Google Keep-inspired)
------------------------------------------------------------
Two pages:
  /        → Todo list  (index.html)
  /notes   → Notes      (keep.html)

No database — everything lives in plain Python lists.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# ---------------------------------------------------------------------------
# IN-MEMORY DATA STORES
# ---------------------------------------------------------------------------

# Each todo looks like: { "id": 1, "text": "Buy milk", "done": False }
todos = []
todo_next_id = 1

# Each note looks like: { "id": 1, "body": "Call dentist tomorrow", "color": "#ffffff" }
# color is the hex code chosen in the palette — defaults to white.
notes = []
note_next_id = 1


# ---------------------------------------------------------------------------
# TODO ROUTES  →  "/"
# ---------------------------------------------------------------------------

@app.route("/")
def todo_page():
    """Show the todo list."""
    return render_template("index.html", todos=todos, active="todo")


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
