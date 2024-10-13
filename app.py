from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create a ToDo model (Table)
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ToDo {self.task}>"


# Home route - displays all tasks
@app.route('/')
def index():
    tasks = ToDo.query.order_by(ToDo.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

# Route to add new task
@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    if new_task:
        task = ToDo(task=new_task)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = ToDo.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

# Route to mark task as complete
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = ToDo.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect(url_for('index'))

# Route to edit a task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = ToDo.query.get(task_id)
    if request.method == 'POST':
        new_task = request.form.get('task')
        if new_task:
            task.task = new_task
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    # Create the database if it doesn't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
