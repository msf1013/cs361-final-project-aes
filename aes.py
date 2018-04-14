# AES algorithm
import sys
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

# Retrieve command line arguments and parse them into options
options = get_options(sys.argv)

# --keysize: Either 128 or 256 bits
key_size = int(options['--keysize'])
# --keyfile: Name of file containing the key
key_file= options['--keyfile']
# --inputfile: Name of file containing plaintext/ciphertext to process
input_file = options['--inputfile']
# --outputfile: Name of file containing the resulting plaintext/ciphertext
output_file = options['--outputfile']
# --mode: Either 'encrypt' or 'decrypt'
mode = options['--mode']

# Call encryption or decryption algorithm accordingly
if mode == 'encrypt':
    encrypt()
else:
    decrypt()