import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def text_to_binary(message):
    """Convert a string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_text(binary_message):
    """Convert a binary string to a text string."""
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message(image_path, message, output_path='hidden_message.png'):
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
        return f"Message hidden successfully in {output_path}."
    except Exception as e:
        return f"Error: {str(e)}"

def reveal_message(image_path):
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
    except Exception as e:
        return f"Error: {str(e)}"

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("500x400")

        # Label and Buttons for Hiding and Revealing messages
        self.label = tk.Label(root, text="Steganography Tool", font=("Arial", 20))
        self.label.pack(pady=10)

        # Hide Message Section
        self.hide_label = tk.Label(root, text="Hide Message in Image")
        self.hide_label.pack(pady=5)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=5)
        self.message_entry.insert(0, "Enter message to hide")

        self.select_image_btn = tk.Button(root, text="Select Image", command=self.select_image_for_hiding)
        self.select_image_btn.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Image with Hidden Message", command=self.save_image_with_message)
        self.save_button.pack(pady=5)

        # Reveal Message Section
        self.reveal_label = tk.Label(root, text="Reveal Message from Image")
        self.reveal_label.pack(pady=20)

        self.select_image_reveal_btn = tk.Button(root, text="Select Image to Reveal Message", command=self.select_image_for_revealing)
        self.select_image_reveal_btn.pack(pady=5)

        self.result_text = tk.Label(root, text="", font=("Arial", 12), wraplength=400)
        self.result_text.pack(pady=10)

    def select_image_for_hiding(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.result_text.config(text=f"Selected Image: {os.path.basename(self.image_path)}")

    def save_image_with_message(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty!")
            return
        if not hasattr(self, 'image_path'):
            messagebox.showerror("Error", "No image selected!")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            result = hide_message(self.image_path, message, output_path)
            self.result_text.config(text=result)

    def select_image_for_revealing(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            result = reveal_message(image_path)
            self.result_text.config(text=f"Revealed Message: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
