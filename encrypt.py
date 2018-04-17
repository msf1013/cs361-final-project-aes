from common import s_box, gfp_2, gfp_3

# Iterate over ciphertext data blocks and apply decryption algorithm
# according to AES standard.
# Returns encrypted list of bytes.
def encrypt(input_bytes, expanded_key, key_size, n_r):
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

# Encrypt block of 16 bytes
def cipher(input_bytes, key_size, expanded_key, n_r):
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
            state[i][j] = s_box[ state[i][j] ]
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
                  state[2][i]        ^ state[3][i]
        temp[1] = state[0][i]        ^ gfp_2[state[1][i]] ^ \
                  gfp_3[state[2][i]] ^ state[3][i]
        temp[2] = state[0][i]        ^ state[1][i] ^ \
                  gfp_2[state[2][i]] ^ gfp_3[state[3][i]]
        temp[3] = gfp_3[state[0][i]] ^ state[1][i] ^ \
                  state[2][i]        ^ gfp_2[state[3][i]]
        
        # Copy to state
        for j in range(0, 4):
            state[j][i] = temp[j]
    
    return state
