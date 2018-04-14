def encrypt(input_bytes, expanded_key, key_size):
    # Add padding if necessary
    if len(input_bytes) % 16 != 0:
        input_bytes.extend([b'\0'] * (16 - (len(input_bytes) % 16)))
    # Encrypt each block of input plaintext
    output_bytes = []
    for i in range(0, len(input_bytes), 16):
        output_bytes += cipher(input_bytes[i:i+16], expanded_key)
    return output_bytes