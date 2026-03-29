# QR Generator

A Python CLI tool to generate QR codes with optional embedded images.

## Requirements

- Python 3.7+
- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow](https://pypi.org/project/pillow/)

Install dependencies:

```bash
pip install qrcode[pil] Pillow
```

## Usage

Run the script and follow the interactive prompts:

```bash
python generate_qr.py
```

The CLI will guide you through three steps:

1. **Text input** - Type text directly or read from a file
2. **Image embedding** (optional) - Provide a png/jpg image to embed in the center of the QR code
3. **Output path** - Choose where to save the generated QR code (defaults to `output_qr.png`)

### Example session

```
=== QR Code Generator ===

How would you like to provide the text?
  1. Type it directly
  2. Read from a file
Choose [1/2] (default: 1): 1
Enter the text to encode: https://github.com

Embed an image in the center of the QR code? [y/N]: y
Enter the image path (png/jpg): logo.png

Output file path (default: output_qr.png): my_qr.png

QR code saved to: my_qr.png
```

### Notes

- When embedding an image, the QR code uses high error correction (H level) to remain scannable despite the center being covered.
- The embedded image is automatically resized to fit within 25% of the QR code area.
- Supported image formats for embedding: PNG, JPG, and other formats supported by Pillow.
