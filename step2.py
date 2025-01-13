import json
import argparse
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def load_public_key(public_key):
    """
    Load a public key from a PEM file.

    Args:
        public_key (str): Path to the public key file. default="account.pub"

    Returns:
        public_key: The loaded public key.
    """
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )
    return public_key


def base64url_encode(data):
    """
    Perform base64 URL encoding.

    Args:
        data (bytes): The data to encode.

    Returns:
        str: The base64 URL encoded string.
    """
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def public_key_to_jwk(public_key):
    """
    Convert a public key to a JSON Web Key (JWK).

    Args:
        public_key : The public key to convert.

    Returns:
        dict: The public key in JWK format.
    """
    # Ensure it's an RSA public key
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("Only RSA public keys are supported.")

    # Get the public key components
    numbers = public_key.public_numbers()

    # Convert modulus and exponent to bytes and base64 URL encode
    n = base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, byteorder='big'))
    e = base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, byteorder='big'))


    # Construct the JWK
    jwk = {
        "jwk": {
        "e": e, # exponent in base64utl encoding
        "kty": "RSA",
        "n": n,  # modulus in base64utl encoding
        }
    }

    # Optional fields for additional data
    jwk["use"] = "sig"  # This is commonly used for signing purposes, you can adjust this as needed
    jwk["alg"] = "RS256" 

    # Return the JWK as a dictionary
    return jwk


def save_jwk_header(jwk, jwk_file):
    """
    Save the JWK to a file.

    Args:
        jwk (dict): The JWK to save.
        jwk_file (str): The path to the JWK file.
    """
    with open(jwk_file, "w") as f:
        json.dump(jwk, f, indent=4)
    print(f"JWK saved to {jwk_file}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert a public key to a JSON Web Key (JWK) format."
    )
    #parser.add_argument("public_key_file", help="Path to the public key file (PEM format).")
    parser.add_argument("--public_key", "-PUB", default="account.pub", help="Path to the public key file (PEM format, default: public_account.key).")
    parser.add_argument("--jwk_file", default="acme_account.jkw", help="Path to save the JWK file, default=acme_account.jwt")
    
    args = parser.parse_args()

    # Load public key from file
    public_key = load_public_key(args.public_key)

    # Convert the public key to JWK
    jwk = public_key_to_jwk(public_key)

    # Save the JWK to a file
    save_jwk_header(jwk, args.jwk_file)


if __name__ == "__main__":
    main()
