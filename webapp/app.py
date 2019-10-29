# web-app for API image manipulation

from flask import Flask, request, render_template, send_from_directory
import os, uuid
import numpy as np
from PIL import Image, ImageDraw, ImageOps

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# default access page
@app.route("/")
def main():
    return render_template('index.html')


# upload selected image and forward to processing page
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/uploads')

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    filename = generate_uuid4_filename(upload.filename)
    print("File name: {}".format(filename))

    # file support verification
    ext = os.path.splitext(filename)[1].lower()
    if (ext == ".jpg") or (ext == ".jpeg") or (ext == ".png") or (ext == ".bmp"):
        print("File accepted")
    else:
        return render_template("error.html", message="The selected file is not supported"), 400

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)

    # open uniao Image
    uniao = Image.open("static/images/uniao.png").convert("RGBA")
    uniao_h, uniao_w = uniao.size

    # Open the input image, convert to RGBA
    img = Image.open(destination).convert("RGBA")

    # resize and crop input img to uniao size
    img = ImageOps.fit(img, (uniao_w, uniao_h), method=Image.ANTIALIAS)

    # Create same size alpha layer with circle
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)

    m = 10
    draw.pieslice([m, m, uniao_h - m, uniao_w - m], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)
    npImage = np.array(img.convert("RGB"))

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    res = Image.fromarray(npImage)

    # paste uniao
    res.paste(uniao, (0, 0), uniao)

    destination_uniao = "/".join([target, filename + ".uniao.png"])
    res.save(destination_uniao)

    # forward to processing page
    return render_template("result.html", image_name=filename)


# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)


def generate_uuid4_filename(filename):
    """
    Generates a uuid4 (random) filename, keeping file extension

    :param filename: Filename passed in. In the general case, this will
                     be provided by django-ckeditor's uploader.
    :return: Randomized filename in urn format.
    :rtype: str
    """
    discard, ext = os.path.splitext(filename)
    basename = uuid.uuid4().urn
    return ''.join([basename, ext])


if __name__ == "__main__":
    app.run()
