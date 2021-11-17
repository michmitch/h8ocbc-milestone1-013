"""
Modul utama untuk server
"""

# Module yang dibutuhkan
from flask import render_template
import config

# Instance App
connex_app = config.connex_app

# Membaca file swagger.yml untuk endpoint
connex_app.add_api("swagger.yml")


# Home directory
@connex_app.route("/")
def home():
    """
    Fungsi untuk home directory
    Akan melakukan render template home.html
    """
    return render_template("home.html")

if __name__ == "__main__":
    connex_app.run(debug=True)
