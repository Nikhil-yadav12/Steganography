# Steganography
This is a simple Python-based steganography tool that allows you to hide a secret message within an image and later retrieve it. The message is encoded in the least significant bits (LSB) of the image pixels.

#Features
Hide a message in an image: Convert a text message into binary and hide it within the pixel values of an image.
Reveal a hidden message: Extract the hidden binary message from the image and convert it back to text.

#Requirements
Python 3.x
Pillow (Python Imaging Library fork)
You can install Pillow using pip:
pip install Pillow


#Usage
1. Hiding a Message in an Image
To hide a message in an image, use the hide action followed by the image path, the message to hide, and an optional output path for the image with the hidden message.

python stegno.py hide <image_path> <message> [output_path]

#Example:
python stegno.py hide input_image.png "This is a secret message!" output_image.png

input_image.png: The original image you want to hide the message in.
"This is a secret message!": The message to hide inside the image.
output_image.png: The output image where the hidden message will be stored (optional, default is hidden_message.png).

2. Revealing a Hidden Message
To extract a hidden message from an image, use the reveal action followed by the image path.

python stegno.py reveal <image_path>
Example:
python stegno.py reveal output_image.png
output_image.png: The image containing the hidden message.
The extracted message will be printed to the console.

#How It Works
Hiding a Message:

The message is converted into a binary string.
The length of the message is also encoded as the first 32 bits.
Each bit of the message is embedded into the least significant bit (LSB) of the image's pixels.

Revealing a Message:

The LSB of each pixel is read to reconstruct the binary message.
The first 32 bits are extracted to determine the length of the hidden message.
The binary string is converted back to text.
#Notes
The message is hidden within the image's least significant bits, so the image may appear almost identical to the original.
The message length must be within the capacity of the image. If the message is too large, an error will occur.


#Limitations
The tool works with grayscale and RGB images.
Large messages may require a larger image to fit without issues.


#License
This project is open-source and released under the MIT License.

