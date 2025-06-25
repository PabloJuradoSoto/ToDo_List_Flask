from flask import Flask, request, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join("database", "app.sqlite")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    if not task_name.strip() or not task_description.strip():
        return redirect(url_for('index'))
    
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

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        conn = get_db_connection()
        conn.execute('UPDATE users SET task_name = ?, task_description = ? WHERE id = ?',
        (task_name, task_description, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        conn.close()
        return render_template('edit.html', task=task)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

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