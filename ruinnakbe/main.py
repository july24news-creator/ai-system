from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import datetime
import os

__version__ = "0.4.0"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Use an absolute path for the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_current_timestamp():
  """Gets the current timestamp and formats it."""
  now = datetime.datetime.now()
  formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
  return formatted_timestamp

def get_uploaded_files():
  """Gets a list of uploaded files."""
  if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
  # Filter out the .gitkeep file
  files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f != '.gitkeep']
  return files

def process_command(command):
    """Processes a user command."""
    if command.lower() == 'list files':
        files = get_uploaded_files()
        if not files:
            return "No files found."
        return "<br>".join(files)
    elif command.lower() == 'clear uploads':
        files = get_uploaded_files()
        for file in files:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        return "All uploaded files have been deleted."
    else:
        return f"Unknown command: {command}"

@app.route('/')
def index():
  """Renders the main page with the current timestamp and version."""
  timestamp = get_current_timestamp()
  files = get_uploaded_files()
  return render_template('index.html', timestamp=timestamp, version=__version__, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        # Handle filename conflicts
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            filename = f"{base}_{counter}{extension}"
            counter += 1
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

@app.route('/command', methods=['POST'])
def handle_command():
    command = request.form.get('command')
    if command:
        result = process_command(command)
        flash(result)
    return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)
