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

The CLI will guide you through four steps:

1. **Text input** - Type text directly or read from a file
2. **Image embedding** (optional) - Provide a png/jpg image to embed in the center of the QR code
3. **Output path** - Choose where to save the generated QR code (defaults to `output_qr.png`)
4. **Compression level** - Choose PNG compression level 0-9 (all lossless), then review the estimated file size before saving

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

PNG compression level (all levels are lossless):
  0 = no compression (largest file, fastest)
  6 = default
  9 = max compression (smallest file, slowest)
Choose [0-9] (default: 6): 0

Estimated file size: 1.25 MB
Save? [Y/n]: y
QR code saved to: my_qr.png
```

### Notes

- When embedding an image, the QR code uses high error correction (H level) to remain scannable despite the center being covered.
- The embedded image is kept at its original resolution. The QR code is scaled up to accommodate it, so there is no quality loss.
- PNG compression is fully lossless at all levels (0-9). Lower levels produce larger files faster; higher levels produce smaller files slower.
- The estimated file size is shown before saving so you can adjust the compression level if needed.
- Supported image formats for embedding: PNG, JPG, and other formats supported by Pillow.
