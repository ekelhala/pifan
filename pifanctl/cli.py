import argparse
import sys

from pifanctl.client import Client

class CLI:

    def __init__(self):

        self.parser = argparse.ArgumentParser("pifanctl", description="Control and monitor the pifan daemon")
        subparsers = self.parser.add_subparsers(dest="command")
        subparsers.required = True

        get_speed = subparsers.add_parser("get_speed", help="Get current fan speed")
        get_speed.set_defaults(func=self._get_speed_cmd)

        get_status = subparsers.add_parser("status", help="Get daemon status")
        get_status.set_defaults(func=self._get_status_cmd)

    def _empty_response_handler(self):
        print("empty response from daemon")

    def _get_client(self) -> Client:
        try:
            client = Client()
        except Exception as e:
            print(f"connection error: {e}")
            sys.exit(1)
        return client

    def _get_speed_cmd(self, client: Client):
        response = client.send_command("get_speed")
        if response:
            print(f"Fan speed: {response['data']['fan_speed']*100}%")
        else: self._empty_response_handler()

    def _get_status_cmd(self, client: Client):
        response = client.send_command("get_status")
        if response:
            print(f"Fan speed>> {response['data']['fan_speed']*100}%\nSystem temperature>> {response['data']['system_temperature']}C")
        else: self._empty_response_handler()

    def run(self):
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            client = self._get_client()
            args.func(client)
            client.destroy()
        else:
            self.parser.print_help()
