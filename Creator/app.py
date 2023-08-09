from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Replace with your database connection details
server = 'DESKTOP-7L5H9VI'
database = 'response'
driver = '{SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};'

def create_connection():
    return pyodbc.connect(connection_string)

def get_current_event_id(connection):
    # Fetch the latest EventID from the EventQ table
    query = "SELECT MAX(EventID) AS MaxEventID FROM EventQ"
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        return row.MaxEventID if row.MaxEventID is not None else 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_questions = int(request.form['num_questions'])
        connection = create_connection()
        current_event_id = get_current_event_id(connection) + 1
        return render_template('form.html', num_questions=num_questions, current_event_id=current_event_id)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    num_questions = int(request.form['num_questions'])
    current_event_id = int(request.form['current_event_id'])
    connection = create_connection()
    for i in range(1, num_questions + 1):
        question = request.form[f'question_{i}']
        qtype = request.form[f'qtype_{i}']
        # Save the question, qtype, and current_event_id into the database table named EventQ
        insert_query = "INSERT INTO EventQ (EventID, Question, QType) VALUES (?, ?, ?)"
        with connection.cursor() as cursor:
            cursor.execute(insert_query, (current_event_id, question, qtype))
            connection.commit()

    return f"Successfully submitted for EventID: {current_event_id}"

if __name__ == '__main__':
    app.run(debug=True)