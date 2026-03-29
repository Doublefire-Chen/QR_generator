import io
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


def get_compress_level():
    """Prompt user for PNG compression level."""
    print("\nPNG compression level (all levels are lossless):")
    print("  0 = no compression (largest file, fastest)")
    print("  6 = default")
    print("  9 = max compression (smallest file, slowest)")
    choice = input("Choose [0-9] (default: 6): ").strip()
    if not choice:
        return 6
    if not choice.isdigit() or int(choice) > 9:
        print("Invalid choice, using default (6).")
        return 6
    return int(choice)


def format_size(size_bytes):
    """Format byte count as a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def generate_qr(text, image_path=None, output_path="output_qr.png", compress_level=6):
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

        # Scale QR up so the logo fits at original resolution within 25% of QR area.
        # This preserves full logo quality instead of downscaling it.
        qr_width, qr_height = img.size
        min_qr_size = int(max(logo.width, logo.height) / 0.25)

        if min_qr_size > max(qr_width, qr_height):
            img = img.resize((min_qr_size, min_qr_size), Image.NEAREST)
            qr_width, qr_height = img.size

        # Center the logo on the QR code at original resolution
        pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)
        img.paste(logo, pos, logo)

    # Estimate file size by writing to memory first
    buf = io.BytesIO()
    img.save(buf, format="PNG", compress_level=compress_level)
    file_size = buf.tell()
    print(f"\nEstimated file size: {format_size(file_size)}")

    confirm = input("Save? [Y/n]: ").strip().lower()
    if confirm in ("n", "no"):
        print("Aborted.")
        return

    with open(output_path, "wb") as f:
        f.write(buf.getvalue())
    print(f"QR code saved to: {output_path}")


def main():
    print("=== QR Code Generator ===")

    text = get_text_input()
    image_path = get_image_input()
    output_path = get_output_path()
    compress_level = get_compress_level()

    generate_qr(text, image_path, output_path, compress_level)


if __name__ == "__main__":
    main()
