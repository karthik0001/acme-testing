import subprocess
import os
import argparse

def check_openssl_installed():
    """
    Check if OpenSSL is installed and available in the system's PATH.
    """
    try:
        subprocess.run(["openssl", "version"], check=True, capture_output=True)
        #print("OpenSSL is installed and available.")
    except FileNotFoundError:
        raise EnvironmentError("OpenSSL is not installed or not in the PATH. Please install OpenSSL and try again.")
    except subprocess.CalledProcessError:
        raise EnvironmentError("Error while checking OpenSSL installation. Ensure OpenSSL is correctly installed.")

def generate_account_key(account_key_file):
    # Generate account private key
    if os.path.exists(account_key_file):
        print(f"Account private key already exists: {account_key_file}")
    else:
        print(f"Generating account private key: {account_key_file}")
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "RSA", "-out", account_key_file, "-pkeyopt", "rsa_keygen_bits:2048"],
            check=True
        )

def extract_public_key(account_key_file, public_account_key_file):
    #Extract the account public key from account private key file using OpenSSL.

    # Check if the account private key file exists
    if not os.path.exists(account_key_file):
        raise FileNotFoundError(f"Account private key file does not exist: {account_key_file}")

    # Check if the account public key file already exists
    if os.path.exists(public_account_key_file):
        print(f"Account public key file already exists: {public_account_key_file}")
        return

    # Extract the account public key
    print(f"Extracting account public key from {account_key_file} to {public_account_key_file}...")
    subprocess.run(
        ["openssl", "rsa", "-in", account_key_file, "-pubout", "-out", public_account_key_file],
        check=True
    )
    print(f"Account Public key saved to: {os.path.abspath('account.pub')}")

def generate_domain_csr_and_key(common_name, country=None, state=None, city=None, organization=None, org_unit=None, email=None, key_file="domain.key", csr_file="domain.csr"):
    """
    Generate a private key and CSR using OpenSSL if they don't already exist.

    Args:
        common_name (str): Common Name (CN) for the certificate.
        country (str): Country Name (C) (2-letter code).
        state (str): State or Province Name (ST).
        city (str): Locality Name (L).
        organization (str): Organization Name (O).
        org_unit (str): Organizational Unit Name (OU).
        #email (str): Email Address.
        key_file (str): Path to save the private key.
        csr_file (str): Path to save the CSR.
    """

    # Construct the subject string
    subject = f"/CN={common_name}"
    if country:
        subject += f"/C={country}"
    if state:
        subject += f"/ST={state}"
    if city:
        subject += f"/L={city}"
    if organization:
        subject += f"/O={organization}"
    if org_unit:
        subject += f"/OU={org_unit}"
    # if email:
    #     subject += f"/emailAddress={email}"

    # Generate domain private key
    if os.path.exists(key_file):
        print(f"Domain private key already exists: {key_file}")
    else:
        print(f"Generating domain private key: {key_file}")
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "RSA", "-out", key_file, "-pkeyopt", "rsa_keygen_bits:2048"],
            check=True
        )

    # Generate CSR
    if os.path.exists(csr_file):
        print(f"CSR already exists: {csr_file}")
    else: 
        print(f"Generating CSR: {csr_file}")
        subprocess.run(
            ["openssl", "req", "-new", "-key", key_file, "-out", csr_file, "-subj", subject],
            check=True
        )

    print("Process completed.")
    print(f"Account private Key (used for signing): {os.path.abspath('account.key')}")
    print(f"Account public Key (convert to JWK for ACME): {os.path.abspath('account.pub')}")
    print(f"Domain private Key: {os.path.abspath(key_file)}")
    print(f"CSR: {os.path.abspath(csr_file)}")
    

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate a private keys and Certificate Signing Request (CSR) using OpenSSL."
    )
    parser.add_argument("common_name", help="Common Name (e.g., domain name) for the certificate.")
    parser.add_argument("--country", "-C", help="Country Name (2-letter code).")
    parser.add_argument("--state", "-ST", help="State or Province Name.")
    parser.add_argument("--city", "-L", help="Locality Name (City).")
    parser.add_argument("--organization", "-O", help="Organization Name.")
    parser.add_argument("--org_unit", "-OU", help="Organizational Unit Name.")
    #parser.add_argument("--email", "-E", help="Email Address.")
    parser.add_argument("--key_file", "-K", default="domain.key", help="File to save the private key (default: domain.key).")
    parser.add_argument("--csr_file", "-R", default="domain.csr", help="File to save the CSR (default: domain.csr).")

    # Parse arguments
    args = parser.parse_args()

    # Ensure OpenSSL is installed 
    check_openssl_installed()

    # Generate account key
    generate_account_key("account.key")
    extract_public_key("account.key", "account.pub")

    # Call the function with parsed arguments
    generate_domain_csr_and_key(
        common_name=args.common_name,
        country=args.country,
        state=args.state,
        city=args.city,
        organization=args.organization,
        org_unit=args.org_unit,
        #email=args.email,
        key_file=args.key_file,
        csr_file=args.csr_file
    )


