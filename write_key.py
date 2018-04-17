# Write key to file
output_file = open("key", "wb")
output_bytes = bytearray.fromhex("00000000000000000000000000000000")
output_file.write(output_bytes)
output_file.close()