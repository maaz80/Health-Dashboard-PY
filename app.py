import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Used for session encryption

# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # If user data exists in session, retrieve it
    user_name = session.get('userName', 'User')
    user_age = session.get('userAge', 'Unknown')
    user_file = session.get('uploadedFile', '/static/images/default-profile.jpg')  # Default image path

    # Check if the mobile menu should be open
    is_menu_open = session.get('isMenuOpen', False)

    return render_template('index.html', 
                           user_name=user_name, 
                           user_age=user_age, 
                           user_file=user_file, 
                           is_menu_open=is_menu_open)

@app.route('/toggle_menu', methods=['POST'])
def toggle_menu():
    # Toggle the mobile menu visibility
    is_menu_open = not session.get('isMenuOpen', False)
    session['isMenuOpen'] = is_menu_open
    return redirect(url_for('index'))

@app.route('/set_user_data', methods=['POST'])
def set_user_data():
    # Get form data
    user_name = request.form.get('userName', 'User')
    user_age = request.form.get('userAge', 'Unknown')
    uploaded_file = request.files.get('uploadedFile')

    # If file is uploaded and is allowed, save it
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('static', filename=f'uploads/{filename}')
    else:
        file_url = '/static/images/default-profile.jpg'  # Default image path

    # Store user data in session
    session['userName'] = user_name
    session['userAge'] = user_age
    session['uploadedFile'] = file_url
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
