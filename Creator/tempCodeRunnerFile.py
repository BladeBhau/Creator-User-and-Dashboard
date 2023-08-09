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

@app.route('/', methods=['GET', 'POST'])
def index():
    num_questions = 0
    if request.method == 'POST':
        num_questions = int(request.form['num_questions'])
        questions_data = []
        for i in range(1, num_questions + 1):
             question = request.form.get(f'question_{i}')
             q_type = request.form.get(f'q_type_{i}')
             questions_data.append((question, q_type))

        with create_connection() as conn:
             with conn.cursor() as cursor:
                cursor.executemany(
                    'INSERT INTO EventQ (Question, QType) VALUES (?, ?)',
                    questions_data
                )
             conn.commit()

    return render_template('index.html', num_questions=num_questions)


if __name__ == '__main__':
    app.run(debug=True)
