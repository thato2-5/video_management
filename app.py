import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from models import db, Video
from config import Config
from datetime import datetime
import humanize

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'video' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('video')
        
        for file in files:
            if file.filename == '':
                flash('No selected file')
                continue
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create unique filename to avoid conflicts
                unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                # Save file
                file.save(file_path)
                
                # Get file size
                file_size = os.path.getsize(file_path)
                
                # Create video record
                video = Video(
                    filename=unique_filename,
                    original_filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    selected=False
                )
                
                db.session.add(video)
        
        db.session.commit()
        flash('Videos uploaded successfully!')
        return redirect(url_for('videos'))
    
    return render_template('upload.html')

@app.route('/videos')
def videos():
    all_videos = Video.query.all()
    selected_videos = Video.query.filter_by(selected=True).all()
    return render_template('videos.html', 
                         all_videos=all_videos, 
                         selected_videos=selected_videos,
                         humanize=humanize)

@app.route('/select_video/<int:video_id>', methods=['POST'])
def select_video(video_id):
    video = Video.query.get_or_404(video_id)
    video.selected = not video.selected
    db.session.commit()
    return jsonify({'selected': video.selected})

@app.route('/delete_video/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    
    # Delete file from filesystem
    if os.path.exists(video.file_path):
        os.remove(video.file_path)
    
    db.session.delete(video)
    db.session.commit()
    flash('Video deleted successfully!')
    return redirect(url_for('videos'))

@app.route('/save_selected', methods=['POST'])
def save_selected():
    # This endpoint is for saving the selection state
    # The selection is already saved when toggling via select_video
    flash('Selection saved successfully!')
    return redirect(url_for('videos'))

@app.template_filter('natural_size')
def natural_size_filter(value):
    return humanize.naturalsize(value)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

