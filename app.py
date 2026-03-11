import os
import sys
import time
import redis
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

# *** FIX 1: PATH RESOLUTION ***
# Add the project directory to Python's search path 
sys.path.append(str(Path(__file__).resolve().parent)) 

# Imports that rely on the local files:
from config import REDIS_URL, QUEUE_NAME
from utils import setup_logging

# Imports for RQ Queue and Retry mechanism
from rq import Queue, Retry 

# Local project imports
from tasks import resize_image 

# --- Configuration ---
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Setup the Flask application
app = Flask(__name__, template_folder='templates') 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging and ensure images directory exists
setup_logging()
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Setup the Redis connection and RQ queue
redis_conn = redis.from_url(REDIS_URL)
queue = Queue(QUEUE_NAME, connection=redis_conn)

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 1. Check file and filename validity
        if 'file' not in request.files:
            return redirect(request.url) 
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            
            # Create a unique input path
            filename_parts = original_filename.rsplit('.', 1)
            temp_filename = f"original_{timestamp}_{filename_parts[0]}.{filename_parts[1]}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
            
            # Save file
            try:
                file.save(input_path)
            except Exception as e:
                app.logger.error(f"Failed to save file to {input_path}: {e}")
                return f"Error saving file: {e}", 500

            # Get resize dimensions
            try:
                width = int(request.form.get('width'))
                height = int(request.form.get('height'))
            except (ValueError, TypeError):
                return "Invalid dimensions submitted.", 400

            # 4. Enqueue the job with Retry configuration (max 3 tries, 10-second interval)
            job = queue.enqueue(
                resize_image, 
                input_path, 
                width, 
                height,
                result_ttl=86400,
                retry=Retry(max=3, interval=10) 
            )

            # Redirect to a page that shows the job status
            return redirect(url_for('job_status', job_id=job.id))

    return render_template('upload.html')

@app.route('/status/<job_id>')
def job_status(job_id):
    job = queue.fetch_job(job_id)

    if job is None:
        return f'Job ID {job_id} not found.', 404

    status = job.get_status()
    # In case of scheduled retry, show a waiting message. Otherwise, show the final result path.
    result_path = job.result if job.is_finished else f'Current Status: {status} (Please wait...)'
    
    return render_template('status.html', job_id=job_id, status=status, result_path=result_path)

@app.route('/dashboard')
def dashboard():
    # Simple dashboard route
    queue_len = queue.count
    workers = queue.workers
    
    return f"""
    <!doctype html>
    <title>RQ Dashboard</title>
    <h1>RQ Dashboard</h1>
    <p>Queue Name: {queue.name}</p>
    <p>Jobs in Queue: {queue_len}</p>
    <p>Workers Online: {len(workers)}</p>
    <hr>
    <p><a href="/">Back to Upload</a></p>
    """

if __name__ == '__main__':
    # *** CRITICAL FIX FOR THE BUILDERROR ***
    # This block defines the 'images' endpoint so the HTML can generate links to resized files.
    app.add_url_rule(
        f'/{UPLOAD_FOLDER}/<path:filename>', 
        endpoint='images', 
        view_func=app.send_static_file,
        defaults={'root': os.path.abspath(UPLOAD_FOLDER)}
    )
    
    app.run(host="0.0.0.0", port=10000, debug=True, use_reloader=False)