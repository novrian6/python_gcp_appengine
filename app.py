from flask import Flask, render_template
from google.cloud import storage
from datetime import timedelta
import os

app = Flask(__name__)

@app.route('/')
def home():
    bucket_name = os.environ.get('BUCKET_NAME')
    image_name = os.environ.get('IMAGE_NAME')
    if not bucket_name or not image_name:
        return "Bucket name or image name not configured.", 400
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(image_name)
    image_url = blob.generate_signed_url(version="v4", expiration=timedelta(minutes=15), method="GET")
    
    return render_template('index.html', image_url=image_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
