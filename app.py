from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Define the folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def pdf_to_word(pdf_path, word_path):
    # Dummy implementation for example
    # Make sure to define your actual PDF to Word conversion logic here
    from convert import pdf_to_word as convert_pdf_to_word
    convert_pdf_to_word(pdf_path, word_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        output_file = file_path.replace('.pdf', '.docx')
        pdf_to_word(file_path, output_file)
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=os.path.basename(output_file))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
