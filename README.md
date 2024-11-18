# Steganography App

## Description

The **Steganography App** is a GUI-based program that allows users to hide secret messages inside image files and extract them later. It utilizes **steganography** to encode text messages within the pixel data of an image, modifying the least significant bits of the RGB values. The app features a simple and intuitive interface built with PyQt5.

---

## Features

- **Select Image:** Load an image file to use for hiding or extracting secret data.
- **Embed Data:** Hide a secret message inside the selected image.
- **Extract Data:** Retrieve a hidden message from an image, if present.

---

## Libraries Used

1. **PyQt5**

   - For building the graphical user interface (GUI).
   - Widgets like `QLabel`, `QPushButton`, `QProgressBar`, and `QTextEdit` are utilized.

2. **Pillow (PIL)**
   - For handling image processing.
   - Used to read, manipulate, and save images.

---

## How It Works

### Hiding Data (Embedding)

1. Convert the secret message into a binary string.
2. Append an **End of File (EOF) marker** (`1111111111111110`) to the binary data to signify the end of the message.
3. Open the selected image and access its pixel data.
4. Replace the **least significant bit (LSB)** of the RGB values of the pixels with bits from the binary message.
5. Save the modified image as a new file.

### Retrieving Data (Extracting)

1. Open the encoded image and access its pixel data.
2. Read the LSBs of the RGB values of the pixels sequentially.
3. Construct a binary string until the EOF marker is encountered.
4. Convert the binary string back to text to retrieve the hidden message.

---

## Installation and Setup

1. **Install Required Libraries**  
   Run the following commands in your terminal or command prompt:

   ```bash
   pip install PyQt5
   pip install pillow
   ```

2. **Run the Program**  
   Save the script as `steganography_app.py` and execute it:
   ```bash
   python steganography_app.py
   ```

---

## How to Use

1. **Open the Application:** Launch the program by running the script.
2. **Select an Image:**
   - Click the "Select Image" button to choose an image file (PNG, BMP, JPG, or JPEG).
3. **Embed Data:**
   - Enter a secret message in the text area.
   - Click "Embed Data" to hide the message inside the image.
   - The modified image will be saved as `output_image.png` in the current directory.
4. **Extract Data:**
   - Click "Extract Data" to retrieve a hidden message from the selected image.
   - The extracted message will appear in the text area.

---

## Notes

- **Image Format:** PNG or BMP is recommended for preserving data integrity, as JPEG compression may lose the hidden information.
- **Message Length:** Ensure the image has enough pixels to encode your message. The number of embeddable characters depends on the image size.

---

## Example Workflow

1. **Embedding:**
   - Input message: `Hello, World!`
   - EOF marker: `1111111111111110`
   - Binary data stored in the image:
     ```
     01001000 01100101 01101100 01101100 01101111 00101100 00100000 01010111 01101111 01110010 01101100 01100100 00100001 1111111111111110
     ```
2. **Extracting:**
   - Binary data read from the image is converted back into the text `Hello, World!`.

---

## Author

## **Vaishnavi Dornala**
