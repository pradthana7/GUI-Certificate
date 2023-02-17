###############################################REFERRENCE: CHAT GPT###########################################################

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Get the public key
public_key = private_key.public_key()

# Serialize the private key
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize the public key
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Write the private key to a file
with open('private_key.pem', 'wb') as file:
    file.write(private_pem)

# Write the public key to a file
with open('public_key.pem', 'wb') as file:
    file.write(public_pem)

###############################################REFERRENCE: CHAT GPT###########################################################
