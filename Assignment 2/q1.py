import string

def encrypt_char(ch, shift1, shift2):
    if ch in string.ascii_lowercase:
        if ch <= 'm':  # case 0
            shift = shift1 * shift2
            enc = chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
            return "0" + enc
        else:  # case 1
            shift = -(shift1 + shift2)
            enc = chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
            return "1" + enc

    elif ch in string.ascii_uppercase:
        if ch <= 'M':  # case 2
            shift = -shift1
            enc = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            return "2" + enc
        else:  # case 3
            shift = shift2 ** 2
            enc = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            return "3" + enc

    return ch   # unchanged chars (space, numbers, punctuation)


def decrypt_char_stream(stream, shift1, shift2):
    # expects stream starting with marker + encrypted char
    marker, ch = stream[0], stream[1]

    if marker == "0":  # lowercase a-m (forward shift)
        shift = -(shift1 * shift2)
        return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))

    elif marker == "1":  # lowercase n-z (backward shift)
        shift = shift1 + shift2
        return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))

    elif marker == "2":  # uppercase A-M (backward shift)
        shift = shift1
        return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))

    elif marker == "3":  # uppercase N-Z (forward shift)
        shift = -(shift2 ** 2)
        return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))

    else:
        return marker   # just return the char if it's not a marker


def encrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            encrypted_line = ""
            for ch in line:
                encrypted_line += encrypt_char(ch, shift1, shift2)
            f_out.write(encrypted_line)


def decrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:
        content = f_in.read()
        i = 0
        decrypted = ""
        while i < len(content):
            if content[i] in "0123" and i + 1 < len(content):  # marker + char
                decrypted += decrypt_char_stream(content[i:i+2], shift1, shift2)
                i += 2
            else:
                decrypted += content[i]
                i += 1
        f_out.write(decrypted)


def verify_files(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, \
         open(file2, "r", encoding="utf-8") as f2:
        if f1.read() == f2.read():
            print("Decryption successful! The files match.")
        else:
            print("Decryption failed! The files do not match.")


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file("Assignment 2/raw_text.txt", "Assignment 2/encrypted_text.txt", shift1, shift2)
    decrypt_file("Assignment 2/encrypted_text.txt", "Assignment 2/decrypted_text.txt", shift1, shift2)
    verify_files("Assignment 2/raw_text.txt", "Assignment 2/decrypted_text.txt")


if __name__ == "__main__":
    main()
