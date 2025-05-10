import socket
import argparse
import json
import sys

SOCKET_PATH = "/tmp/pifan.sock"

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
                return None
            return response_dict
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_error(response):
    print(response["status"], response["message"])

def get_speed_cmd():
    response = send_command("get_speed")
    if response:
        print(f"Fan speed: {response['data']['fan_speed']*100}%")

def get_status_cmd():
    response = send_command("get_status")
    if response:
        print(f"""Fan speed>> {response['data']['fan_speed']*100}%\n
              System temperature>> {response['data']['system_temperature']}C""")

def main():
    parser = argparse.ArgumentParser("pifanctl", description="Control and monitor the pifan daemon")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    get_speed = subparsers.add_parser("get_speed", help="Get current fan speed")
    get_speed.set_defaults(func=get_speed_cmd)

    get_status = subparsers.add_parser("status", help="Get daemon status")
    get_status.set_defaults(func=get_status_cmd)

    args = parser.parse_args()
    args.func()

if __name__ == "__main__":
    main()