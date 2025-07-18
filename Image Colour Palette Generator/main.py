import os.path
from PIL import Image
from flask import Flask, abort, render_template, redirect, url_for, flash, request
import numpy as np
from collections import Counter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'
app.config["UPLOAD_FOLDER"] = 'static/uploads'

def get_top_colors(image_path, num_colors=10):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((150, 150))
    pixels = np.array(img).reshape(-1, 3)
    color_counts = Counter([tuple(pixel) for pixel in pixels])
    top_colors = color_counts.most_common(num_colors)
    return [rgb_to_hex(color[0]) for color in top_colors]

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb



@app.route("/", methods=["GET", "POST"])
def home():
    colors = []
    image_url = None
    if request.method == "POST":
        file = request.files['image']
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)

            img = Image.open(image_path)
            img = img.resize((600, 500))
            img.save(image_path)

            colors = get_top_colors(image_path)
            image_url = url_for('static', filename=f'uploads/{file.filename}')
    return render_template("index.html", image_url=image_url, colors=colors)


if __name__ == "__main__":
    app.run(debug=True)