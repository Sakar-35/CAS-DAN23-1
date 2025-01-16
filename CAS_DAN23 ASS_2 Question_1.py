#  GROUP CAS/DAN23
# ARYAN RAYAMAJHI [s385826]
# MEENU DEVI MEENU DEVI [s383485]
# RIWAJ ADHIKARI [s385933]
# SAKAR KHADKA [s385095]

# This Python program performs encryption and decryption on text from a file
def encrypt(raw, n, m):
    encrypted = ""
    for c in raw:
        #Check the given conditions
        if c >= "a" and c <= "m":  # Lowercase (a-m)
            encrypted += chr((ord(c) - ord("a") + (n * m)) % 13 + ord("a"))
        elif c >= "n" and c <= "z":  # Lowercase (n-z)
            encrypted += chr((ord(c) - ord("a") - (n + m)) % 13 + ord("n"))
        elif c >= "A" and c <= "M":  # Uppercase (A-M)
            encrypted += chr((ord(c) - ord("A") - n) % 13 + ord("A"))
        elif c >= "N" and c <= "Z":  # Uppercase (N-Z)
            encrypted += chr((ord(c) - ord("A") + m ** 2) % 13 + ord("N"))
        else:
            encrypted += c  # Special characters and numbers remain unchanged
    return encrypted

def decrypt(encrypted, n, m):
    decrypted = ""
    for c in encrypted:
        #Check the given conditions
        if c >= "a" and c <= "m":  # Lowercase (a-m)
            decrypted += chr((ord(c) - ord("a") - (n * m)) % 13 + ord("a"))
        elif c >= "n" and c <= "z":  # Lowercase (n-z)
            decrypted += chr((ord(c) - ord("a") + (n + m)) % 13 + ord("n"))
        elif c >= "A" and c <= "M":  # Uppercase (A-M)
            decrypted += chr((ord(c) - ord("A") + n) % 13 + ord("A"))
        elif c >= "N" and c <= "Z":  # Uppercase (N-Z)
            decrypted += chr((ord(c) - ord("A") - m ** 2) % 13 + ord("N"))
        else:
            decrypted += c  # Special characters and numbers remain unchanged
    return decrypted

def verify(raw, decrypted):
    # Verify if the decrypted text matches the original text
    return raw == decrypted
# Get user input for the integers n and m
n = int(input("Enter integer n: "))
m = int(input("Enter integer m: "))

# Read the original text from 'raw_text.txt'
with open("raw_text.txt", encoding="utf-8") as file:
    raw_text = file.read()

# Encrypt the content
encrypted_text = encrypt(raw_text, n, m)

# Write encrypted content to encrypted_text.txt
with open("encrypted_text.txt", "w", encoding="utf-8") as file:
    file.write(encrypted_text)

print("Encryption completed and content saved to 'encrypted_text.txt'.")

# Decrypt the content
decrypted_text = decrypt(encrypted_text, n, m)

# Write decrypted content to decrypted_text.txt
with open("decrypted_text.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_text)

print("Decryption completed and content saved to 'decrypted_text.txt'.")
print(f"Decrypted Text: {decrypted_text}")

# Verify the decryption
if verify(raw_text, decrypted_text):
    print("Decryption verified successfully.")
else:
    print("Decryption failed.")
