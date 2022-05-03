if __name__ == "__main__":
    input_path = "plaintext.bin"
    with open(input_path,"rb") as f:
        input = f.read()
    f.close()
    
    input_binary = [bin(c)[2:].rjust(8,'0') for c in input]  # remove '0b' from string, fill 8 bits
    input_binary = ''.join(input_binary)
    print(input_binary)
    print(len(input_binary))