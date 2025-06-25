from flask import Flask, request, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = "/tmp/tareas.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=rows)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (task_name, task_description) VALUES (?, ?)', (task_name, task_description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def pagina_no_encontrada(error):
    return redirect(url_for('index'))

if __name__ == "__main__":
    if not os.path.exists('database'):
        os.mkdir('database')
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_name TEXT NOT NULL,
                        task_description TEXT NOT NULL
                    )
                     ''')
        conn.close()
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)