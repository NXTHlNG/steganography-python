from PIL import Image
import numpy as np

BITS_FOR_MESSAGE_SIZE = 30


def hide_message(img, data):
    # img = Image.open(image_path)
    img_data = np.array(img)

    # data = open(data_path, 'rb').read()
    data_size = len(data)

    # Add the size of the data as the first 30 bits
    size_bits = np.binary_repr(data_size, BITS_FOR_MESSAGE_SIZE)

    # Convert the data to a binary string
    data_bits = ''.join([np.binary_repr(byte, 8) for byte in data])

    # Combine the size and data strings
    message_bits = size_bits + data_bits

    # Flatten the image data
    img_data_flat = img_data.reshape(-1)

    # Set the least significant bit of each element in the flattened array
    img_data_flat[:len(message_bits)] = (img_data_flat[:len(message_bits)] & ~1).astype(np.uint8) | np.array(list(message_bits), dtype=np.uint8)

    # Reshape the modified image data
    img_data = img_data_flat.reshape(img_data.shape)

    # Save the modified image
    img_output = Image.fromarray(img_data, mode="RGB")

    return img_output


def extract_message(img):
    # with Image.open(image_path) as img:
    pixels = np.array(img.getdata())

    if pixels.shape[0] < BITS_FOR_MESSAGE_SIZE // 3:
        raise ValueError("Image is too small to contain a message")

    # Get the size of the hidden message
    size_bits = ''
    for i in range(BITS_FOR_MESSAGE_SIZE // 3):
        r, g, b = pixels[i]
        size_bits += str(r & 1)
        size_bits += str(g & 1)
        size_bits += str(b & 1)

    message_size = int(size_bits, 2)

    # Extract the message bits from the rest of the image
    message_bits = pixels[10:, :].reshape(-1) & 1
    message_bits = message_bits[:message_size * 8]

    # Convert the list of bits to bytes
    message_bytes = np.packbits(message_bits).tobytes()

    # Decode the bytes as ASCII characters
    message = message_bytes.decode('utf-8')

    return message
