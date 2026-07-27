from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)


def get_db_connection():
    con = sqlite3.connect("noted.db")
    con.row_factory = sqlite3.Row
    return con


def create_table():
    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
    """)

    con.commit()
    con.close()


def get_tasks():
    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    con.close()
    return tasks


@app.route("/")
def home():
    tasks = get_tasks()

    return render_template(
        "index.html",
        tasks=tasks,
        error=""
    )


@app.route("/add", methods=["POST"])
def add_task():
    text = request.form["task"]

    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (text, completed)
        VALUES (?, ?)
        """,
        (text, 0)
    )

    con.commit()
    con.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:id>")
def delete_task(id):
    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    con.commit()
    con.close()

    return redirect(url_for("home"))


@app.route("/completed/<int:id>")
def completed_task(id):
    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = NOT completed
        WHERE id=?
        """,
        (id,)
    )

    con.commit()
    con.close()

    return redirect(url_for("home"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    if request.method == "POST":
        new_text = request.form["task"]

        con = get_db_connection()
        cursor = con.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET text=?
            WHERE id=?
            """,
            (new_text, id)
        )

        con.commit()
        con.close()

        return redirect(url_for("home"))

    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
        (id,)
    )

    task = cursor.fetchone()

    con.close()

    return render_template(
        "edit.html",
        task=task,
        id=id
    )


if __name__ == "__main__":

    create_table()
    app.run(debug=True)