import socket
import argparse
import json
import sys

SOCKET_PATH = "/tmp/pifan.sock"
COMMANDS = ["get_speed"]

def send_command(command: str):
    """
    send command to socket
    """
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(SOCKET_PATH)
            client_socket.sendall(json.dumps({"command": command}).encode("utf-8"))
            response = client_socket.recv(4096).decode("utf-8")
            response_dict = json.loads(response)
            if response_dict["status"] == "error":
                print_error(response_dict)
            else:
                print_speed(response_dict)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_speed(response):
    print(response["fan_speed"])

def print_error(response):
    print(response["status"], response["message"])

def main():
    parser = argparse.ArgumentParser("pifanctl")
    parser.add_argument("command")
    args = parser.parse_args()
    if hasattr(args, "command"):
        if args.command in COMMANDS:
            send_command(args.command)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()