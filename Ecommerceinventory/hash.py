import streamlit_authenticator as stauth

# Enter your passwords here
passwords = ['wesal12345', 'rana12345']

# This is the direct way to hash a list in the new version
hashed_passwords = [stauth.Hasher.hash(p) for p in passwords]

print(f"Wesal: {hashed_passwords[0]}")
print(f"Rana: {hashed_passwords[1]}")