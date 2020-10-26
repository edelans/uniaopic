# web-app for API image manipulation

from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)
import os
import uuid
import numpy as np
from PIL import Image, ImageDraw, ImageOps

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# upload selected image and forward to processing page
@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        target = os.path.join(APP_ROOT, "static/images/uploads")

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
            return (
                render_template(
                    "error.html", message="The selected file is not supported"
                ),
                400,
            )

        # save file
        destination = "/".join([target, filename])
        print("File saved to to:", destination)
        upload.save(destination)

        # open uniao Image
        uniao = Image.open("static/images/uniao.png").convert("RGBA")
        uniao_w, uniao_h  = uniao.size

        # Open input image, convert to RGBA, resize and crop input img to uniao size
        img = Image.open(destination).convert("RGBA")
        img = ImageOps.fit(img, (uniao_w, uniao_h), method=Image.LANCZOS)

        # Create same size alpha layer with circle
        alpha = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(alpha)
        margin = 10  # to avoid picture overflowing outside uniao ring
        draw.pieslice(
            [margin, margin, uniao_h - margin, uniao_w - margin], 0, 360, fill=255
        )

        # Convert alpha image and input image to numpy array to add alpha layer to input image
        npAlpha = np.array(alpha)
        npImage = np.array(img.convert("RGB"))
        npImage = np.dstack((npImage, npAlpha))

        # convert back to PIL image
        res = Image.fromarray(npImage)

        # paste uniao and save
        res.paste(uniao, (0, 0), uniao)
        destination_uniao = "/".join([target, filename + ".uniao.png"])
        res.save(destination_uniao)

        ###########################################
        # steps for squared uniao

        # open uniao Image
        uniao = Image.open("static/images/square_uniao.png").convert("RGBA")
        uniao_w, uniao_h  = uniao.size

        # Open input image, convert to RGBA, resize and crop input img to uniao size
        img = Image.open(destination).convert("RGBA")
        img = ImageOps.fit(img, (uniao_w, uniao_h), method=Image.LANCZOS)

        # Create same size alpha layer with square
        alpha = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(alpha)
        margin = 10  # to avoid picture overflowing outside uniao ring
        draw.rectangle(
            [margin, margin, uniao_h - margin, uniao_w - margin], fill=255
        )

        # Convert alpha image and input image to numpy array to add alpha layer to input image
        npAlpha = np.array(alpha)
        npImage = np.array(img.convert("RGB"))
        npImage = np.dstack((npImage, npAlpha))

        # convert back to PIL image
        res = Image.fromarray(npImage)

        # paste uniao and save
        res.paste(uniao, (0, 0), uniao)
        destination_uniao = "/".join([target, filename + ".square.uniao.png"])
        res.save(destination_uniao)



        ###########################################
        # forward to result page
        return redirect(url_for("success", image_name=filename))

    return render_template("index.html")


@app.route("/success/<string:image_name>")
def success(image_name):
    return render_template("result.html", image_name=image_name)


# retrieve file from 'static/images' directory
@app.route("/static/images/<filename>")
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
    return "".join([basename, ext])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
