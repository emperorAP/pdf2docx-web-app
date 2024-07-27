from flask import Flask, request, render_template, send_file, url_for, redirect
from werkzeug.utils import secure_filename
import os
from convert import pdf_to_word  # Import the conversion function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None
    error_message = None
    if request.method == 'POST':
        if 'pdf-file' not in request.files:
            error_message = "No file part in the request."
        else:
            file = request.files['pdf-file']
            if file.filename == '':
                error_message = "No selected file."
            elif file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    word_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename.rsplit('.', 1)[0] + '.docx')
                    file.save(pdf_path)
                    pdf_to_word(pdf_path, word_path)
                    download_link = url_for('download_file', filename=filename.rsplit('.', 1)[0] + '.docx')
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
            else:
                error_message = "Invalid file type. Only PDF files are allowed."

    return render_template('index.html', download_link=download_link, error_message=error_message)

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])
    app.run(debug=True)
