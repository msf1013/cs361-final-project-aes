#!/usr/bin/env python3

"""AES Python implementation

This script implement the AES encryption and decryption procedures defined in
https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

This implementation specifically uses the ECB mode, and conforms to the
standard algorithms in FIPS 197.

The script expects the following arguments:

   1) keysize: An integer, either 128 or 256, representing the key size in
               bits.
   2) keyfile: Name of file containing the key.
   3) inputfile: Name of file containing input plaintext/ciphertext to process,
                 depending on whether mode is encrypt/decrypt.
   4) outputfile: Name of file where the output plaintext/ciphertext will be
                  produced, depending on whether mode is encrypt/decrypt.
   5) mode: A string, either 'encrypt' or 'decrypt'.
"""

import sys
import array
from common import expand_key
from encrypt import encrypt
from decrypt import decrypt

# Parse arguments
# https://gist.github.com/dideler/2395703
def get_options(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-' and argv[0][1] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

def main():
    # Retrieve command line arguments and parse them into options
    options = get_options(sys.argv)

    # --keysize: Either 128 or 256 bits
    key_size = int(options['--keysize'])
    # --keyfile: Name of file containing the key
    key_file_name = options['--keyfile']
    # --inputfile: Name of file containing plaintext/ciphertext to process
    input_file_name = options['--inputfile']
    # --outputfile: Name of file containing the resulting plaintext/ciphertext
    output_file_name = options['--outputfile']
    # --mode: Either 'encrypt' or 'decrypt'
    mode = options['--mode']

    # Read input files
    input_file = open(input_file_name, "rb")
    key_file = open(key_file_name, "rb")
    output_file = open(output_file_name, "wb")

    input_bytes = bytearray(input_file.read())
    key_bytes = bytearray(key_file.read())

    # Generate expanded key
    n_k = 0
    n_r = 0
    if key_size == 128:
        n_k = 4
        n_r = 10
    elif key_size == 256:
        n_k = 8
        n_r = 14
    expanded_key = expand_key(key_bytes, n_k, n_r)

    # Call encryption or decryption algorithm accordingly
    if mode == 'encrypt':
        output_bytes = encrypt(input_bytes, expanded_key, n_r)
    else:
        output_bytes = decrypt(input_bytes, expanded_key, n_r)

    # Write output to file
    output_bytes = array.array('B', output_bytes)
    output_file.write(output_bytes)

    # Close files
    input_file.close()
    key_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
