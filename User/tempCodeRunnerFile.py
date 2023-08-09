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

if __name__ == '__main__':
    app.run(debug=True)
