from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF for PDF handling
import os

app = Flask(__name__)

# Function to dynamically list all DBQ PDFs in the directory
def get_available_dbqs():
    dbq_directory = os.getcwd()  # Get current directory
    dbq_files = [f for f in os.listdir(dbq_directory) if f.startswith("dbq_") and f.endswith(".pdf")]
    dbq_names = {file: file.replace("dbq_", "").replace("_", " ").replace(".pdf", "").title() for file in dbq_files}
    return dbq_names

@app.route('/')
def index():
    dbqs = get_available_dbqs()
    if not dbqs:
        return "No DBQ files found. Please upload VA DBQs."
    
    form_html = '''
    <form action="/generate" method="post">
        <label for="name">Name:</label>
        <input type="text" name="name" required><br>
        
        <label for="dob">Date of Birth:</label>
        <input type="text" name="dob" required><br>
        
        <label for="service_branch">Service Branch:</label>
        <input type="text" name="service_branch" required><br>
        
        <label for="dbq_choice">Select DBQ:</label>
        <select name="dbq_choice">
    '''
    for file, name in dbqs.items():
        form_html += f'<option value="{file}">{name}</option>'
    
    form_html += '''
        </select><br>
        
        <label for="va_rating">VA Rating Percentage:</label>
        <input type="number" name="va_rating" required><br>
        
        <input type="submit" value="Generate DBQ">
    </form>
    '''
    
    return form_html

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    dob = request.form['dob']
    service_branch = request.form['service_branch']
    dbq_choice = request.form['dbq_choice']
    
    # Ensure the selected DBQ exists
    if not os.path.exists(dbq_choice):
        return "DBQ form not found. Please ensure the file is uploaded.", 404
    
    pdf = fitz.open(dbq_choice)
    page = pdf[0]
    
    # Insert user details into the PDF
    page.insert_text((100, 700), f"Name: {name}", fontsize=12, color=(0, 0, 0))
    page.insert_text((400, 700), f"DOB: {dob}", fontsize=12, color=(0, 0, 0))
    page.insert_text((100, 680), f"Service Branch: {service_branch}", fontsize=12, color=(0, 0, 0))
    
    output_filename = f"filled_{dbq_choice}"
    pdf.save(output_filename)
    pdf.close()
    
    return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
