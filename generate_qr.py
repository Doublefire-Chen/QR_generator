import sys
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_M
from PIL import Image


def get_text_input():
    """Prompt user for text to encode in the QR code."""
    print("\nHow would you like to provide the text?")
    print("  1. Type it directly")
    print("  2. Read from a file")
    choice = input("Choose [1/2] (default: 1): ").strip()

    if choice == "2":
        path = input("Enter the file path: ").strip()
        if not os.path.isfile(path):
            print(f"Error: File not found: {path}")
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            print("Error: File is empty.")
            sys.exit(1)
        print(f"Read {len(text)} characters from {path}")
        return text

    text = input("Enter the text to encode: ").strip()
    if not text:
        print("Error: Text cannot be empty.")
        sys.exit(1)
    return text


def get_image_input():
    """Prompt user for an optional image to embed in the QR code center."""
    embed = input("\nEmbed an image in the center of the QR code? [y/N]: ").strip().lower()
    if embed not in ("y", "yes"):
        return None

    path = input("Enter the image path (png/jpg): ").strip()
    if not os.path.isfile(path):
        print(f"Error: Image not found: {path}")
        sys.exit(1)
    return path


def get_output_path():
    """Prompt user for the output file path."""
    path = input("\nOutput file path (default: output_qr.png): ").strip()
    if not path:
        path = "output_qr.png"
    if not path.lower().endswith(".png"):
        path += ".png"
    return path


def generate_qr(text, image_path=None, output_path="output_qr.png"):
    """Generate a QR code, optionally embedding an image in the center."""
    # Use high error correction when embedding an image so the QR stays scannable
    error_correction = ERROR_CORRECT_H if image_path else ERROR_CORRECT_M

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    if image_path:
        logo = Image.open(image_path).convert("RGBA")

        # Resize logo to fit within ~25% of the QR code area (safe for scanning)
        qr_width, qr_height = img.size
        max_logo_size = int(qr_width * 0.25)
        logo_ratio = min(max_logo_size / logo.width, max_logo_size / logo.height)
        new_size = (int(logo.width * logo_ratio), int(logo.height * logo_ratio))
        logo = logo.resize(new_size, Image.LANCZOS)

        # Center the logo on the QR code
        pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)
        img.paste(logo, pos, logo)

    img.save(output_path)
    print(f"\nQR code saved to: {output_path}")


def main():
    print("=== QR Code Generator ===")

    text = get_text_input()
    image_path = get_image_input()
    output_path = get_output_path()

    generate_qr(text, image_path, output_path)


if __name__ == "__main__":
    main()
