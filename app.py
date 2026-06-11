"""
app.py — Daily Activity Tracker
--------------------------------
A beginner-friendly Flask app that lets you log daily habits,
mark them as complete, and get a quick progress summary.

No database needed — we use a plain Python list that lives in
memory while the server is running.
"""

import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------------------------------------------------------------------
# DATA STORE
# ---------------------------------------------------------------------------
# We keep all activities in a simple Python list of dictionaries.
# Each item looks like:  { "id": 1, "name": "Morning run", "done": False }
# This resets every time you restart the server — perfect for a beginner demo.

activities = []

# A counter so every activity gets a unique ID even after deletions.
next_id = 1

# ---------------------------------------------------------------------------
# QUOTES
# ---------------------------------------------------------------------------
# A hand-picked list of short, uplifting quotes.
# random.choice() picks one at random each time the page loads.

QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Small daily improvements over time lead to stunning results.", "Robin Sharma"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Discipline is the bridge between goals and accomplishment.", "Jim Rohn"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Success is the sum of small efforts repeated day in and day out.", "Robert Collier"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
]


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """
    Landing page.

    PROGRESS CALCULATION:
    - We count how many activities have 'done' set to True.
    - The total is just the length of the list.
    - We pass both numbers to the template so it can render the summary.

    RANDOM QUOTE:
    - random.choice(QUOTES) returns a random (text, author) tuple every
      time this function runs — which is every page load or refresh.
    """
    completed = sum(1 for a in activities if a["done"])  # count True entries
    total = len(activities)
    quote_text, quote_author = random.choice(QUOTES)

    return render_template(
        "index.html",
        activities=activities,
        completed=completed,
        total=total,
        quote_text=quote_text,
        quote_author=quote_author,
    )


@app.route("/add", methods=["POST"])
def add_activity():
    """
    Receive the form submission and append a new activity to the list.
    We strip() the input so accidental leading/trailing spaces don't sneak in.
    """
    global next_id

    name = request.form.get("activity_name", "").strip()

    if name:  # only add if the user actually typed something
        activities.append({
            "id": next_id,
            "name": name,
            "done": False,
        })
        next_id += 1

    return redirect(url_for("index"))


@app.route("/toggle/<int:activity_id>", methods=["POST"])
def toggle_activity(activity_id):
    """
    Flip the 'done' flag on a single activity.
    We search by ID so position in the list doesn't matter.
    """
    for activity in activities:
        if activity["id"] == activity_id:
            activity["done"] = not activity["done"]  # True → False, False → True
            break

    return redirect(url_for("index"))


@app.route("/delete/<int:activity_id>", methods=["POST"])
def delete_activity(activity_id):
    """
    Remove an activity permanently from the list.
    list() creates a new list that excludes the matching item.
    """
    global activities
    activities = [a for a in activities if a["id"] != activity_id]
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=True means the server auto-reloads when you save app.py.
    # Turn it off in production.
    app.run(debug=True)
