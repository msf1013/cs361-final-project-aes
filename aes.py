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
input_file  = open(input_file_name, "rb")
key_file    = open(key_file_name, "rb")
output_file = open(output_file_name, "wb")

input_bytes = bytearray(input_file.read())
key_bytes = bytearray(key_file.read())

# Generate expanded key
expanded_key = expand_key(key_bytes, key_size)

# Call encryption or decryption algorithm accordingly
if mode == 'encrypt':
    output_bytes = encrypt(input_bytes, expanded_key, key_size)
else:
    output_bytes = decrypt(input_bytes, expanded_key, key_size)

# Write output to file
output_bytes = array.array('B', output_bytes)
output_file.write(output_bytes)

# Close files
input_file.close()
key_file.close()
output_file.close()