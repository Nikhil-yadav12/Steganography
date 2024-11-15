from PIL import Image
import sys

def text_to_binary(message):
    """Convert a string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_text(binary_message):
    """Convert a binary string to a text string."""
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message(image_path, message, output_path='hidden_message.png'):
    """
    Hides a message within an image using steganography.

    Parameters:
        image_path (str): Path to the input image.
        message (str): The message to hide.
        output_path (str): Path to save the output image with the hidden message.

    Raises:
        FileNotFoundError: If the input image file does not exist.
        ValueError: If the message is too long for the image.
    """
    try:
        image = Image.open(image_path)
        width, height = image.size

        # Convert message to binary and prefix it with its length
        binary_message = text_to_binary(message)
        message_length = len(binary_message)
        binary_message = format(message_length, '032b') + binary_message  # 32 bits for length

        # Ensure message fits in the image
        if message_length > width * height * (3 if image.mode == 'RGB' else 1):
            raise ValueError("Message is too long to fit in the image.")

        binary_index = 0
        for y in range(height):
            for x in range(width):
                if binary_index >= len(binary_message):
                    break
                pixel = image.getpixel((x, y))

                # If the image is grayscale, pixel is an integer
                if isinstance(pixel, int):
                    bit = int(binary_message[binary_index])
                    pixel = (pixel & ~1) | bit  # Embed the bit in the LSB of the pixel
                    image.putpixel((x, y), pixel)
                    binary_index += 1

                # If the image is RGB, pixel is a tuple
                else:
                    pixel = list(pixel)
                    for i in range(len(pixel)):
                        if binary_index < len(binary_message):
                            bit = int(binary_message[binary_index])
                            pixel[i] = (pixel[i] & ~1) | bit  # Embed the bit in the LSB
                            binary_index += 1
                    image.putpixel((x, y), tuple(pixel))  # Update the pixel with new values

        image.save(output_path)
        print(f"Message hidden successfully in {output_path}.")
    except FileNotFoundError:
        print(f"Error: File {image_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def reveal_message(image_path):
    """
    Reveals a hidden message from an image.

    Parameters:
        image_path (str): Path to the input image.

    Returns:
        str: The hidden message.

    Raises:
        FileNotFoundError: If the input image file does not exist.
    """
    try:
        image = Image.open(image_path)
        width, height = image.size

        binary_message = ""
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))

                # If the image is grayscale, pixel is an integer
                if isinstance(pixel, int):
                    binary_message += str(pixel & 1)  # Append the LSB

                # If the image is RGB, pixel is a tuple
                else:
                    for i in range(len(pixel)):
                        binary_message += str(pixel[i] & 1)  # Append the LSB of each channel

        # Extract the length of the message
        message_length = int(binary_message[:32], 2)
        binary_message = binary_message[32:32 + message_length]

        # Convert the binary message back to text
        return binary_to_text(binary_message)
    except FileNotFoundError:
        print(f"Error: File {image_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stegno.py [hide/reveal] <image_path> [message/output_path]")
    else:
        action = sys.argv[1]
        image_path = sys.argv[2]

        if action == "hide" and len(sys.argv) >= 4:
            message = sys.argv[3]
            output_path = sys.argv[4] if len(sys.argv) > 4 else 'hidden_message.png'
            hide_message(image_path, message, output_path)
        elif action == "reveal":
            print("Revealed Message:", reveal_message(image_path))
        else:
            print("Invalid usage. Use 'hide' or 'reveal' with appropriate arguments.")
