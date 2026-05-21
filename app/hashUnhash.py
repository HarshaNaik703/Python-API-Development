import bcrypt

# 1. Setup your password
password = "xyzxyzxyz".encode('utf-8')

# 2. Hash the password
# gensalt() generates a unique salt and includes it in the final hash automatically
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# 3. Verify a password
# For login, check the user's input against the stored hash
user_input = "xyzxyzxyz".encode('utf-8')

if bcrypt.checkpw(user_input, hashed):
    print("Match found! Access granted.")
else:
    print("No match. Access denied.")
