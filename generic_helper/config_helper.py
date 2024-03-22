from configparser import ConfigParser

#https://tutswiki.com/read-write-config-files-in-python/

INI_FILE = "config.ini"

def get_config_value(section:str, key:str)->str:
    """
    Get the value of a key from a configuration file.

    Args:
        section: The name of the section in the configuration file that contains the key.
        key: The name of the key in the configuration file that contains the value.

    Returns:
        The value of the key.
    """

    config_object = ConfigParser()
    config_object.read(INI_FILE)
    return config_object[section][key]

def write_config(section:str, key:str, value:str)->str:
    """
    Write a key-value pair to a configuration file.

    Args:
        section: The name of the section in the configuration file that contains the key.
        key: The name of the key in the configuration file that contains the value.
        value: The value to be written to the configuration file.

    Returns:
        The value of the key.
    """

    config_object = ConfigParser()
    config_object.read(INI_FILE)
    config_object[section][key] = value
    with open(INI_FILE, 'w') as conf:
        config_object.write(conf)
