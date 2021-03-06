# The MIT License (MIT)
#
# Copyright (c) 2018 Mario Sergio Fuentes Juarez and Vishal Gullapalli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""AES Python implementation: decryption procedure

This script contains the methods required for data decryption according to
the AES spec: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf
"""

from common import INV_S_BOX, GFP_9, GFP_11, GFP_13, GFP_14, add_round_key
from common import generate_initial_state

def decrypt(input_bytes, expanded_key, n_r):
    """Decrypts input bytes, producing recovered message based on the provided
        key.

    Iterate over ciphertext data blocks and apply decryption algorithm
    according to AES standard.

    Args:
        input_bytes: A byte array containing message to be decrypted.
        expanded_key: A byte array containing the key schedule.
        key_size: An integer, either 128 or 256.
        n_r: An integer, either 10 or 14, representing the number of rounds
             that the encryption/decryption algorithm will perform.

    Returns:
        A byte array that represents the decrypted message.
    """

    # Decrypt each block of input plaintext
    output_bytes = []
    for i in range(0, len(input_bytes), 16):
        # Decipher block of 16 bytes
        partial = decipher(input_bytes[i:i + 16], expanded_key, n_r)

        # Re-group bytes in column-first order
        for col in range(0, 4):
            for row in range(0, 4):
                output_bytes.append(partial[row][col])

    # Remove padding bytes from output
    output_bytes = output_bytes[:-1 * output_bytes[-1]]

    return output_bytes


# Decrypt block of 16 bytes
def decipher(input_bytes, expanded_key, n_r):
    """Decrypts a data block of 16 bytes, producing a decrypted 4x4 byte matrix
       'state' as explained in the AES standard.

    Args:
        input_bytes: A 16 bytes-long array containing the data block to be
                     decrypted.
        expanded_key: A byte array containing the key schedule.
        n_r: An integer, either 10 or 14, representing the number of rounds
             that the encryption/decryption algorithm will perform.

    Returns:
        A 4x4 byte matrix that contains the decrypted block 'state'.
    """

    state = generate_initial_state(input_bytes)
    state = add_round_key(state, expanded_key, n_r * 4 * 4)

    # Apply rounds of inverse operations as stated in AES standard
    for round_no in range(n_r - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, expanded_key, round_no * 4 * 4)
        state = inv_mix_columns(state)

    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, expanded_key, 0)

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
            state[i][j] = INV_S_BOX[state[i][j]]
    return state


def inv_mix_columns(state):
    temp = [0 for _ in range(0, 4)]

    for i in range(0, 4):
        temp[0] = (GFP_14[state[0][i]] ^ GFP_11[state[1][i]]) ^ \
                  (GFP_13[state[2][i]] ^ GFP_9[state[3][i]])
        temp[1] = (GFP_9[state[0][i]] ^ GFP_14[state[1][i]]) ^ \
                  (GFP_11[state[2][i]] ^ GFP_13[state[3][i]])
        temp[2] = (GFP_13[state[0][i]] ^ GFP_9[state[1][i]]) ^ \
                  (GFP_14[state[2][i]] ^ GFP_11[state[3][i]])
        temp[3] = (GFP_11[state[0][i]] ^ GFP_13[state[1][i]]) ^ \
                  (GFP_9[state[2][i]] ^ GFP_14[state[3][i]])

        # Copy to state
        for j in range(0, 4):
            state[j][i] = temp[j]

    return state
