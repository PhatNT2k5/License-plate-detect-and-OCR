from flask import Flask, request, jsonify, render_template, url_for
import os
from werkzeug.utils import secure_filename
from detect_input_picture import process_license_plate  # Import module xử lý ảnh

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads') # Use a static folder correctly.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/picture')
def picture():
    return render_template('picture.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Xử lý ảnh
            processed_image_path = process_license_plate(filepath)
            
            if processed_image_path:
                # Tạo URL cho ảnh đã xử lý
                processed_image_url = url_for('static', filename=os.path.join('uploads', os.path.basename(processed_image_path)).replace('\\', '/'))
                return jsonify({'processed_image_url': processed_image_url})
            else:
                return jsonify({'error': 'Image processing failed'}), 500
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400



if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)