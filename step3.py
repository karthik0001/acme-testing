import argparse
import requests

def get_replay_nonce(url):
    """
    Makes a GET request to the given URL and retrieves the replay-nonce from response headers.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        str: The replay-nonce value from the response headers.
    """
    try:
        # Perform the GET request
        response = requests.get(url)

        # Check if the response contains the replay-nonce header
        replay_nonce = response.headers.get('Replay-Nonce')

        if replay_nonce:
            return replay_nonce
        else:
            raise ValueError("Replay-Nonce header not found in the response.")

    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Get replay-nonce from ACME.")
    parser.add_argument(
        "--url",
        nargs="?",
        default="https://acme-v02.api.letsencrypt.org/acme/new-nonce",
        help="ACME directory URL for nonce (default is https://acme-v02.api.letsencrypt.org/acme/new-nonce)."
    )
    args = parser.parse_args()

    # Get replay-nonce from the specified URL
    replay_nonce = get_replay_nonce(args.url)

    if replay_nonce:
        print(f"Replay-Nonce: {replay_nonce}")
    else:
        print("Failed to retrieve replay-nonce.")

if __name__ == "__main__":
    main()
