from pathlib import Path
import os

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "quantum-safe-demo-secret"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

BASE_DIR = Path(__file__).parent
ENCRYPTED_DIR = BASE_DIR / "encrypted"
DECRYPTED_DIR = BASE_DIR / "decrypted"

ENCRYPTED_DIR.mkdir(exist_ok=True)
DECRYPTED_DIR.mkdir(exist_ok=True)

QSV_HEADER = b"QSV1"
SALT_SIZE = 16
NONCE_SIZE = 12


def is_strong_password(password):
    return (
        len(password) >= 12
        and any(character.islower() for character in password)
        and any(character.isupper() for character in password)
        and any(character.isdigit() for character in password)
        and any(not character.isalnum() for character in password)
    )


def derive_key(password, salt):
    return Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    ).derive(password.encode("utf-8"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/guide")
def guide():
    return render_template("guide.html")


@app.route("/questions")
def questions():
    return render_template("questions.html")


@app.route("/comparison")
def comparison():
    return render_template("comparison.html")


@app.route("/info")
@app.route("/about")
def info():
    return render_template("info.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/encrypt", methods=["POST"])
def encrypt_file():
    uploaded_file = request.files.get("file")
    mode = request.form.get("mode", "AES-256")
    password = request.form.get("password", "")

    if not uploaded_file or uploaded_file.filename == "":
        flash("Please select a file.")
        return redirect(url_for("home"))

    if not is_strong_password(password):
        flash("Use a password with 12+ characters, upper and lowercase letters, a number, and a symbol.")
        return redirect(url_for("home"))

    filename = secure_filename(uploaded_file.filename)
    original_data = uploaded_file.read()

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    encrypted_data = AESGCM(key).encrypt(nonce, original_data, None)

    encrypted_filename = f"{filename}.qsv"

    encrypted_path = ENCRYPTED_DIR / encrypted_filename
    encrypted_path.write_bytes(QSV_HEADER + salt + nonce + encrypted_data)

    return render_template(
        "result.html",
        title="Encryption Successful",
        message=f"{filename} was encrypted successfully using {mode}.",
        download_url=url_for(
            "download_encrypted", filename=encrypted_filename
        ),
        download_text="Download Encrypted File",
    )


@app.route("/decrypt", methods=["POST"])
def decrypt_file():
    encrypted_file = request.files.get("encrypted_file")
    password = request.form.get("password", "")

    if not encrypted_file or encrypted_file.filename == "" or not password:
        flash("Upload an encrypted file and enter its password.")
        return redirect(url_for("home"))

    try:
        encrypted_name = secure_filename(encrypted_file.filename)
        complete_data = encrypted_file.read()
        if not complete_data.startswith(QSV_HEADER):
            raise ValueError("Unsupported encrypted file format")

        salt_start = len(QSV_HEADER)
        nonce_start = salt_start + SALT_SIZE
        ciphertext_start = nonce_start + NONCE_SIZE
        salt = complete_data[salt_start:nonce_start]
        nonce = complete_data[nonce_start:ciphertext_start]
        ciphertext = complete_data[ciphertext_start:]
        key = derive_key(password, salt)

        original_data = AESGCM(key).decrypt(nonce, ciphertext, None)

        original_name = encrypted_name.removesuffix(".qsv")
        output_path = DECRYPTED_DIR / original_name
        output_path.write_bytes(original_data)

        return render_template(
            "result.html",
            title="Decryption Successful",
            message=f"{original_name} was restored successfully.",
            download_url=url_for(
                "download_decrypted", filename=original_name
            ),
            download_text="Download Restored File",
        )

    except Exception:
        flash("Decryption failed. Check that the correct password is being used.")
        return redirect(url_for("home"))


@app.route("/download/encrypted/<filename>")
def download_encrypted(filename):
    return send_file(ENCRYPTED_DIR / secure_filename(filename), as_attachment=True)


@app.route("/download/decrypted/<filename>")
def download_decrypted(filename):
    return send_file(DECRYPTED_DIR / secure_filename(filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)