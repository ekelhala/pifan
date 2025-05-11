import argparse
import sys

from pifanctl.client import Client
from pifanctl.cli import CLI

def main():
    CLI().run()

if __name__ == "__main__":
    main()