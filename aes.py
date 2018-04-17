#!/usr/bin/env python3

# AES algorithm
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
    expanded_key = expand_key(key_bytes, key_size, n_k, n_r)
    
    # Call encryption or decryption algorithm accordingly
    if mode == 'encrypt':
        output_bytes = encrypt(input_bytes, expanded_key, key_size, n_r)
    else:
        output_bytes = decrypt(input_bytes, expanded_key, key_size, n_r)
    
    # Write output to file
    output_bytes = array.array('B', output_bytes)
    output_file.write(output_bytes)
    
    # Close files
    input_file.close()
    key_file.close()
    output_file.close()

if __name__ == '__main__':
    main()