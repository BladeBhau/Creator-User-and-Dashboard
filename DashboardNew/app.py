from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Replace with your SQL Server connection details
server = 'DESKTOP-7L5H9VI'
database = 'response'
driver = '{SQL Server}'



def get_answers(event_id):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    query = f"SELECT Question, Answer FROM Results WHERE EventID = {event_id}"
    cursor.execute(query)
    answers = [{"question": row.Question, "answer": row.Answer} for row in cursor]

    cursor.close()
    connection.close()
    return answers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        answers = get_answers(event_id)

        return render_template(
            'dashboard.html',
            event_id=event_id,
            answers=answers
        )

    return render_template('dashboard_input.html')

if __name__ == '__main__':
    app.run(debug=True)
