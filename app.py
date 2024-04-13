from flask import Flask, request, jsonify, render_template, url_for
from werkzeug.utils import secure_filename
import os
from count import process_image  # Make sure this import is correct

app = Flask(__name__)
app = Flask(__name__, static_folder='static')


# Configuration for file upload and storage directories
UPLOAD_FOLDER = 'uploads'  # Adjust as needed, make sure this directory exists
STATIC_FOLDER = 'static'   # Typically, 'static' is used to serve static files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
@app.route('/')  # Root or Home
def index():
    return render_template('index.html')

@app.route('/data')  # Data page using about.html
def data():
    return render_template('about.html')

@app.route('/contact')  # Contact page
def contact():
    return render_template('contact.html')

@app.route('/about_me')  # About Me page
def about_me():
    return render_template('danny.html')  # Assuming 'danny.html' is your About Me page


@app.route('/get-about-text')
def get_about_text():
    text_path = 'static/about_context.txt'
    try:
        with open(text_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found.", 404


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'image' not in request.files:
            return jsonify({'message': "No file part in the request"}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'message': "No selected file"}), 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        model_path = 'pretrained_models/best_model_7.pth'
        output_path = os.path.join(app.config['STATIC_FOLDER'], 'density_' + filename)
        estimated_count, density_map_path = process_image(filepath, model_path, output_path)

        if estimated_count == -1:
            return jsonify({'message': "Error processing image"}), 500

        density_map_url = url_for('static', filename=os.path.basename(density_map_path))
        return jsonify({
            'message': "Image processed successfully",
            'count': float(estimated_count),
            'densityMap': density_map_url
        })
    except Exception as e:
        print(f"Error during upload: {str(e)}")
        return jsonify({'message': f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Default port to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port, debug=False)  # Turn off debug for production
