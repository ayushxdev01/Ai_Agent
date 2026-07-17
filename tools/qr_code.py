"""
tools/qr_code.py
Generates a QR code image from text/URL and saves it, returning a file path.
"""

import qrcode
import os
import uuid

OUTPUT_DIR = "static/qr_codes"


def execute(arguments: dict):
    text = arguments.get("text")

    if not text:
        return "QR code error: need 'text' (a URL or any text to encode)"

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"qr_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        img = qrcode.make(text)
        img.save(filepath)

        return f"QR code generated successfully. Access it at: /qr_codes/{filename}"

    except Exception as e:
        return f"QR code error: {e}"


if __name__ == "__main__":
    print(execute({"text": "https://github.com/ayushxdev01"}))