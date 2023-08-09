from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Replace with your SQL Server connection details
server = 'DESKTOP-7L5H9VI'
database = 'response'
driver = '{SQL Server}'

# Function to fetch questions from the database for a given EventID
def get_questions(event_id):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    query = f"SELECT Question, QType FROM EventQ WHERE EventID = {event_id}"
    cursor.execute(query)
    questions = [{"question": row.Question, "qtype": row.QType} for row in cursor]

    cursor.close()
    connection.close()
    return questions

def insert_event_result(event_id, question, answer):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    query = "INSERT INTO Results (EventID, Question, Answer) VALUES (?, ?, ?)"
    cursor.execute(query, (event_id, question, answer))

    connection.commit()
    cursor.close()
    connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        event_id = request.form['event_id']

        try:
            event_id = int(event_id)
            questions = get_questions(event_id)
            return render_template('questions.html', event_id=event_id, questions=questions)
        except ValueError:
            return "Invalid EventID. Please enter a valid numeric EventID."

    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    event_id = int(request.form['event_id'])

    for question in request.form:
        if question != 'event_id':
            answer = request.form[question]
            insert_event_result(event_id, question, answer)

    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)