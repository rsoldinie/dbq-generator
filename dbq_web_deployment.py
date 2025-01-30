from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF for PDF handling
import os

app = Flask(__name__)

# Ensure using the most up-to-date DBQ forms
DBQ_FILES = {
    "Knee and Lower Leg Conditions": "latest_dbq_knee.pdf",
    "Shoulder and Arm Conditions": "latest_dbq_shoulder.pdf"
}

@app.route('/')
def index():
    return '''
    <form action="/generate" method="post">
        <label for="name">Name:</label>
        <input type="text" name="name" required><br>
        
        <label for="dob">Date of Birth:</label>
        <input type="text" name="dob" required><br>
        
        <label for="service_branch">Service Branch:</label>
        <input type="text" name="service_branch" required><br>
        
        <label for="dbq_choice">Select DBQ:</label>
        <select name="dbq_choice">
            <option value="Knee and Lower Leg Conditions">Knee and Lower Leg Conditions</option>
            <option value="Shoulder and Arm Conditions">Shoulder and Arm Conditions</option>
        </select><br>
        
        <label for="va_rating">VA Rating Percentage:</label>
        <input type="number" name="va_rating" required><br>
        
        <input type="submit" value="Generate DBQ">
    </form>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    dob = request.form['dob']
    service_branch = request.form['service_branch']
    dbq_choice = request.form['dbq_choice']
    va_rating = int(request.form['va_rating'])
    
    pdf_filename = DBQ_FILES.get(dbq_choice)
    if not pdf_filename or not os.path.exists(pdf_filename):
        return "DBQ form not found.", 404
    
    pdf = fitz.open(pdf_filename)
    page = pdf[0]
    
    # Insert user details i

