from common import inv_sbox, gfp9, gfp11, gfp13, gfp14

def decrypt(input_bytes, expanded_key, key_size):
    # Encrypt each block of input plaintext
    output_bytes = []
    for i in range(0, len(input_bytes), 16):
        partial = decipher(input_bytes[i:i+16], key_size, expanded_key)
        
        for c in range(0, 4):
            for r in range(0, 4):
                output_bytes.append(partial[r][c])
    
    output_bytes = output_bytes[: -1 * output_bytes[-1] ]

    return output_bytes

def decipher(input_bytes, key_size, expanded_key):
    n_r = 0
    if key_size == 128:
        n_r = 10
    elif key_size == 256:
        n_r = 14
    
    state = [[0 for _ in range(0, 4)] for _ in range(0,4)]
    next = 0
    for j in range(0, 4):
        for i in range(0, 4):
            state[i][j] = input_bytes[next]
            next += 1
    
    state = add_round_key(state, expanded_key, n_r * 4 * 4)
    
    for round in range(n_r - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, expanded_key, round * 4 * 4)
        state = inv_mix_columns(state)
    
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, expanded_key, 0)
    
    return state

def add_round_key(state, expanded_key, index):
    
    for j in range(0, 4):
        for i in range(0, 4):
            state[i][j] = state[i][j] ^ expanded_key[index]
            index += 1
    return state

def inv_shift_rows(state):
    temp = [0 for _ in range(0, 4)]
    for i in range(1, 4):
        for j in range(0, 4):
            temp[(j + i) % 4] = state[i][j]
        for j in range(0, 4):
            state[i][j] = temp[j]    
    return state

def inv_sub_bytes(state):
    for j in range(0, 4):
        for i in range(0, 4):
            state[i][j] = inv_sbox[ state[i][j] ]
    return state

def inv_mix_columns(state):
    temp = [0 for _ in range(0, 4)]
    
    for i in range(0, 4):
        temp[0] = (gfp14[state[0][i]] ^ gfp11[state[1][i]]) ^ \
                  (gfp13[state[2][i]] ^ gfp9[state[3][i]])
        temp[1] = (gfp9[state[0][i]] ^ gfp14[state[1][i]]) ^ \
                  (gfp11[state[2][i]] ^ gfp13[state[3][i]])
        temp[2] = (gfp13[state[0][i]] ^ gfp9[state[1][i]]) ^ \
                  (gfp14[state[2][i]] ^ gfp11[state[3][i]])
        temp[3] = (gfp11[state[0][i]] ^ gfp13[state[1][i]]) ^ \
                  (gfp9[state[2][i]] ^ gfp14[state[3][i]])
        
        for j in range(0, 4):
            state[j][i] = temp[j]
    
    return state
