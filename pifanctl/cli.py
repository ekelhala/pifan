import argparse
import sys

from pifanctl.client import Client

class CLI:

    def __init__(self):

        self.parser = argparse.ArgumentParser("pifanctl", description="Control and monitor the pifan daemon")
        subparsers = self.parser.add_subparsers(dest="command")
        subparsers.required = True

        get_status = subparsers.add_parser("status", help="Get daemon status")
        get_status.set_defaults(func=self._get_status_cmd)

        get_config = subparsers.add_parser("config", help="Get daemon configuration")
        get_config.set_defaults(func=self._get_config_cmd)

        set_controller = subparsers.add_parser("set_controller", help="Set controller profile, gets reset on daemon restart")
        set_controller.add_argument("controller_name", type=str, help="The name of the controller to use")
        set_controller.set_defaults(func=self._set_controller_cmd)

    def _empty_response_handler(self):
        print("empty response from daemon")

    def _get_client(self) -> Client:
        try:
            client = Client()
        except Exception as e:
            print(f"connection error: {e}")
            sys.exit(1)
        return client

    def _get_status_cmd(self, client: Client, _args):
        response = client.send_command({"command": "get_status"})
        if response:
            print(f"Fan speed>> {response['data']['fan_speed']*100}%")
            print(f"System temperature>> {response['data']['system_temperature']}C")
            print(f"Controller profile>> {response['data']['controller']}")
        else: self._empty_response_handler()

    def _set_controller_cmd(self, client: Client, args):
        response = client.send_command({"command": "set_controller",
                                        "controller_name": args.controller_name})
        if response:
            print(response["data"]["message"])

    def _get_config_cmd(self, client: Client, _args):
        response = client.send_command({"command": "get_config"})
        if response:
            print("configuration\n-------------")
            print(f"temp_high | {response['data']['temp_high']} C")
            print(f"temp_low  | {response['data']['temp_low']} C")
            print(f"gpio_pin  | {response['data']['gpio_pin']}")
            print(f"controller| {response['data']['controller']}")
            print(f"frequency | {response['data']['frequency']} Hz")

    def run(self):
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            client = self._get_client()
            args.func(client, args)
            client.destroy()
        else:
            self.parser.print_help()
