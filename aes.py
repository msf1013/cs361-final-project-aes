# AES algorithm
import sys
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

# Retrieve command line arguments and parse them into options
options = get_options(sys.argv)

# --keysize: Either 128 or 256 bits
key_size         = int(options['--keysize'])
# --keyfile: Name of file containing the key
key_file_name    = options['--keyfile']
# --inputfile: Name of file containing plaintext/ciphertext to process
input_file_name  = options['--inputfile']
# --outputfile: Name of file containing the resulting plaintext/ciphertext
output_file_name = options['--outputfile']
# --mode: Either 'encrypt' or 'decrypt'
mode             = options['--mode']

# Read input files
input_file  = open(input_file_name, "r+")
key_file    = open(key_file_name, "r+")
output_file = open(output_file_name, "w+")

input_string = input_file.read()
key_string   = key_file.read()
input_bytes = bytearray.fromhex(input_string)
key_bytes = bytearray.fromhex(key_string)

# Generate expanded key
expanded_key = expand_key(key_bytes, key_size)

# Call encryption or decryption algorithm accordingly
if mode == 'encrypt':
    output_bytes = encrypt(input_bytes, expanded_key, key_size)
    output_bytes = [ str('%02X' % byte) for byte in output_bytes ]
    output_file.write("".join(output_bytes))
else:
    output_bytes = decrypt(input_bytes, expanded_key, key_size)
    output_bytes = [ str('%02X' % byte) for byte in output_bytes ]
    output_file.write("".join(output_bytes))