import argparse
import sys

from pifanctl.client import Client
from pifanctl.cli import CLI

def main():
    try:
        client = Client()
    except Exception as e:
        print(f"connection error: {e}")
        sys.exit(1)
    cli = CLI(client)
    cli.run()

if __name__ == "__main__":
    main()