from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('patient_data.db')  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # This allows us to treat rows as dictionaries
    return conn

# Home route to view patients
@app.route('/')
def index():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()
    return render_template('index.html', patients=patients)

# Route to add a new patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        address = request.form['address']
        medical_history = request.form['medical_history']
        current_medications = request.form['current_medications']
        
        conn = get_db_connection()
        conn.execute('''INSERT INTO patients (first_name, last_name, age, gender, contact_number, address, medical_history, current_medications) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (first_name, last_name, age, gender, contact_number, address, medical_history, current_medications))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_patient.html')

# Route to delete a patient
@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to update patient details
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    conn = get_db_connection()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        address = request.form['address']
        medical_history = request.form['medical_history']
        current_medications = request.form['current_medications']
        
        conn.execute('''UPDATE patients SET first_name = ?, last_name = ?, age = ?, gender = ?, contact_number = ?, 
                        address = ?, medical_history = ?, current_medications = ? WHERE id = ?''',
                        (first_name, last_name, age, gender, contact_number, address, medical_history, current_medications, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('update_patient.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True)
