# pifan

This daemon provides precise control over a fan that is attached to one of the PWM outputs of Raspberry Pi. With a single configuration file, you can set high and low temperatures, use different control profiles for your fan, or control things like frequency used to drive the fan. This program is built on top of `gpiozero`, which is a Python library available on Raspberry Pi.

## Installation & usage

Currently the daemon can be installed by cloning the repository and using the provided `setup.py`-file. Steps are provided below.

1. **Get the source code**: Clone the repository by running `git clone https://github.com/ekelhala/pifan.git`
2. **Install**: Move to the cloned repository: `cd pifand`, and run `sudo python setup.py install`. This will build and copy all necessary files to right locations.
3. **Set up the systemd service**: We want to run this daemon in the background, so we'll use a systemd service to achieve this. Run `sudo systemctl enable pifan` to enable the service at startup, and `sudo systemctl start pifan` to start the service now. If you have everything set up correctly, your PWM fan connected to Pi's GPIO 12 should start spinning at full speed.
4. **Configure the daemon**: If you want to change how the fan behaves, you should edit the file `/etc/pifan/default.toml` (for example with `nano`: `sudo nano /etc/pifan/default.toml`). After making your changes, remember to run `sudo systemctl restart pifan` to restart the fan service, which also reloads the configuration file you just edited.

## Configuration

*not added yet*

## Controllers

`pifan` provides two controller profiles for your fan: `max_speed` and `linear_interpolator`. The controller you want to use can be selected by setting the value of `controller` under `[fan]` in the configuration file. Default controller is `max_speed`.

### `max_speed` and `linear_interpolator`

The `max_speed`-controller drives the fan at full speed all times, while `linear_interpolator` looks at the current temperature, and increases the speed of the fan linearly when the temperature increases. When using `linear_interpolator`, the fan is turned off, when the current temperature goes below the low temperature (set with `temp_low`). When high temperature (`temp_high` in configuration) is reached, `linear_interpolator` drives the fan at maximum speed.

### Adding new controllers

The structure of the code is designed in a way which makes adding new controllers easy. You can add your controller code under `fan_control` by following the structure of existing controllers, and using the `BaseController` and `ControllerOptions` to operate the controller. After writing your controller, you can make it available through `get_controller`, and a configuration option, which you can set in the configuration file.
