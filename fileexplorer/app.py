from flask import Flask, request, redirect, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Ensure the upload folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    files = []
    for item in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], item)
        if os.path.isdir(path):
            files.append({'name': item, 'type': 'Mapa', 'size': '-'})
        else:
            size_kb = round(os.path.getsize(path) / 1024, 2)
            files.append({'name': item, 'type': 'Datoteka', 'size': size_kb})
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Ni datoteke', 400
    file = request.files['file']
    if file.filename == '':
        return 'Ni izbrane datoteke', 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return redirect('/')

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    new_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    return redirect('/')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)