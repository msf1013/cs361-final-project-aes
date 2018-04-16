from common import sbox, gfp2, gfp3

def encrypt(input_bytes, expanded_key, key_size):
    # Add padding if necessary
    if len(input_bytes) % 16 != 0:
        input_bytes.extend([0] * (16 - (len(input_bytes) % 16)))
    # Encrypt each block of input plaintext
    output_bytes = []
    for i in range(0, len(input_bytes), 16):
        partial = cipher(input_bytes[i:i+16], key_size, expanded_key)
        
        for c in range(0, 4):
            for r in range(0, 4):
                output_bytes.append(partial[r][c])

    return output_bytes

def cipher(input_bytes, key_size, expanded_key):
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
    
    #print("STATE - before")
    #print(state)
    
    state = add_round_key(state, expanded_key, 0)
    
    for round in range(1, n_r):
        #print("STATE - round #%d" % (round))
        #print(state)
        
        state = sub_bytes(state)        
        state = shift_rows(state)        
        # TODO
        state = mix_columns(state)
        
        #print("STATE - round #%d - after mix_columns" % (round))
        #print(state)
        
        state = add_round_key(state, expanded_key, round * 4 * 4)
      
        
    #print("STATE - round #%d" % (10))
    #print(state)
    
    state = sub_bytes(state)
    state = shift_rows(state)
    
    #print("STATE - round #%d - after shift_rows" % (10))
    #print(state)
    
    state = add_round_key(state, expanded_key, n_r * 4 * 4)
    
    #print("STATE - FINAL")
    #print(state)
    
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
            state[i][j] = sbox[ state[i][j] ]
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
        temp[0] = (gfp2[state[0][i]] ^ gfp3[state[1][i]]
                   ^ state[2][i] ^ state[3][i])
        temp[1] = (state[0][i] ^ gfp2[state[1][i]]
                   ^ gfp3[state[2][i]] ^ state[3][i])
        temp[2] = (state[0][i] ^ state[1][i]
                   ^ gfp2[state[2][i]] ^ gfp3[state[3][i]])
        temp[3] = (gfp3[state[0][i]] ^ state[1][i]
                   ^ state[2][i] ^ gfp2[state[3][i]])
        
        for j in range(0, 4):
            state[j][i] = temp[j]
    
    return state
