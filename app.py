from flask import Flask, render_template, request
from PIL import Image, ImageOps, ImageFilter
import base64
import io

app = Flask(__name__)

app.static_folder = 'static'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Menerima file gambar dari formulir HTML
        image = request.files["image"]

        # Membaca gambar menggunakan PIL
        img = Image.open(image)

        # Memproses gambar berdasarkan opsi yang dipilih
        if "blur" in request.form:
            img = img.filter(ImageFilter.BLUR)
        if "flip" in request.form:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if "pixelate" in request.form:
            # Apply pixelization filter
            pixel_size = 10  # Adjust the pixel size as desired
            img = img.resize((img.width // pixel_size, img.height // pixel_size), Image.NEAREST)
            img = img.resize((img.width * pixel_size, img.height * pixel_size), Image.NEAREST)
        if "invert" in request.form:
            img = ImageOps.invert(img)
        if "black_and_white" in request.form:
            img = img.convert("L")  # Convert image to grayscale (black and white)
        if "dark" in request.form:
            img = ImageOps.equalize(img)
        if "contour" in request.form:
            img = img.filter(ImageFilter.CONTOUR)

        # Mengonversi gambar ke format base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Mengirim gambar yang telah diproses ke template HTML
        return render_template("index.html", img_data=img_base64)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
