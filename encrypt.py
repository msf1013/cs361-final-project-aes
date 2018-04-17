from common import s_box, gfp_2, gfp_3

def encrypt(input_bytes, expanded_key, key_size, n_r):
    """Encrypts input bytes, producing a ciphered message based on the provided
        key.
    
    Iterate over ciphertext data blocks and apply enryption algorithm
    according to AES standard.

    Args:
        input_bytes: A byte array containing message to be encrypted.
        expanded_key: A byte array containing the key schedule.
        key_size: An integer, either 128 or 256.
        n_r: An integer, either 10 or 14, representing the number of roungs
             that the encryption/decryption algorithm will perform.

    Returns:
        A byte array that represents the encrypted message.
    """
    
    # Add ZeroLength padding if necessary
    pad = 16 - (len(input_bytes) % 16)
    input_bytes.extend([0] * pad)
    input_bytes[-1] = pad
        
    # Encrypt each block of input plaintext
    output_bytes = []
    for i in range(0, len(input_bytes), 16):
        # Cipher block of 16 bytes
        partial = cipher(input_bytes[i:i+16], key_size, expanded_key, n_r)
        
        # Re-group bytes in column-first order
        for c in range(0, 4):
            for r in range(0, 4):
                output_bytes.append(partial[r][c])

    return output_bytes


def cipher(input_bytes, key_size, expanded_key, n_r):
    """Encrypts a data block of 16 bytes, producing an encrypted 4x4 byte
       matrix 'state' as explained in the AES standard.
    
    Args:
        input_bytes: A 16 bytes-long array containing the data block to be
                     decrypted.
        key_size: An integer, either 128 or 256.
        expanded_key: A byte array containing the key schedule.
        n_r: An integer, either 10 or 14, representing the number of roungs
             that the encryption/decryption algorithm will perform.

    Returns:
        A 4x4 byte matrix that contains the encrypted block 'state'.
    """
    
    state = [[0 for _ in range(0, 4)] for _ in range(0,4)]
    next = 0
    # Grab first 16 bytes of data in column-first order
    for j in range(0, 4):
        for i in range(0, 4):
            state[i][j] = input_bytes[next]
            next += 1
    
    state = add_round_key(state, expanded_key, 0)
    
    # Apply rounds of operations as stated in AES standard
    for round in range(1, n_r):
        state = sub_bytes(state)        
        state = shift_rows(state)        
        state = mix_columns(state)
        state = add_round_key(state, expanded_key, round * 4 * 4)
          
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, expanded_key, n_r * 4 * 4)
    
    return state


def add_round_key(state, expanded_key, index):
    for j in range(0, 4):
        for i in range(0, 4):
            state[i][j] = state[i][j] ^ expanded_key[index]
            index += 1
    return state


def sub_bytes(state):
    for j in range(0, 4):
        for i in range(0, 4):
            state[i][j] = s_box[state[i][j]]
    return state


def shift_rows(state):
    temp = [0 for _ in range(0, 4)]
    for i in range(1, 4):
        for j in range(0, 4):
            temp[j] = state[i][(j + i) % 4]
        for j in range(0, 4):
            state[i][j] = temp[j]    
    return state


def mix_columns(state):
    temp = [0 for _ in range(0, 4)]
    
    for i in range(0, 4):
        temp[0] = gfp_2[state[0][i]] ^ gfp_3[state[1][i]] ^ \
                  state[2][i] ^ state[3][i]
        temp[1] = state[0][i] ^ gfp_2[state[1][i]] ^ \
                  gfp_3[state[2][i]] ^ state[3][i]
        temp[2] = state[0][i] ^ state[1][i] ^ \
                  gfp_2[state[2][i]] ^ gfp_3[state[3][i]]
        temp[3] = gfp_3[state[0][i]] ^ state[1][i] ^ \
                  state[2][i] ^ gfp_2[state[3][i]]
        
        # Copy to state
        for j in range(0, 4):
            state[j][i] = temp[j]
    
    return state
