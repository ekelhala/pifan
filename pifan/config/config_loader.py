import tomllib
import logging

def load_config(path: str = "/etc/pifan/config.toml") -> dict | None:
    """
    Loads the given config file as this program's configuration.
    Returns the configuration as dict if successful, or None if not
    The path defaults to /etc/pifan/config.toml

    The resulting dict will look like this:
    ```
    {
       "fan": {
           "temp_low": float,
           "temp_high": float,
           "controller": string,
           "gpio_pin": string
       },
       "daemon": {
          "update_interval": int
       }
    }
    ```
    """
    try:
        with open(path, "rb") as config_file:
            config = tomllib.load(config_file)
            logging.info(f"config file {path} loaded")
            return config
    except FileNotFoundError:
        logging.error(f"config file {path} not found")
        return None
    except tomllib.TOMLDecodeError as e:
        logging.error(f"error when parsing config file {path}: ", e)

def _validate_config(config: dict) -> bool:
    """
    Validates the given config, returns `True` if the config is valid, `False` otherwise
    """
    