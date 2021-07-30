"""
Configuration object source file
"""

import sys
import configparser


def oops(arg_text):
    print("\n***** Oops, {} *****\n".format(arg_text))
    sys.exit(86)


def get_config_string(arg_config, arg_section, arg_key):
    """
    get one STRING configuration parameter by key
    """
    parm_value = "?"
    try:
        parm_value = arg_config.get(arg_section, arg_key)
    except Exception as err:
        oops("get_config_string: config file key {}, reason: {}"
             .format(arg_key, repr(err)))
    print("get_config_string: {} = {}".format(arg_key, parm_value))
    return parm_value


def get_config_int(arg_config, arg_section, arg_key, ):
    """
    get one INTEGER configuration parameter by key
    """
    parm_value = -1
    try:
        parm_value = arg_config.getint(arg_section, arg_key)
    except Exception as err:
        oops("get_config_int: config file key {}, reason: {}"
             .format(arg_key, repr(err)))
    print("get_config_int: {} = {}".format(arg_key, parm_value))
    return parm_value


def get_config_float(arg_config, arg_section, arg_key):
    """
    get one FLOAT configuration parameter by key
    """
    parm_value = -1.0
    try:
        parm_value = arg_config.getfloat(arg_section, arg_key)
    except Exception as err:
        oops("get_config_float: config file key {}, reason: {}"
             .format(arg_key, repr(err)))
    print("get_config_float: {} = {}".format(arg_key, parm_value))
    return parm_value


class ConfigObject:
    """
    Class definition for the configuration object.
    """

    def __init__(self, arg_config_path):
        """
        Get all of the configuration parameters.
        """
        print("ConfigObject: Begin")
        try:
            config = configparser.ConfigParser()
            config.read(arg_config_path)
            section = config.sections()[0]
            print("get_config_all: config file {} was loaded"
                   .format(arg_config_path))
        except Exception as err:
            oops("get_config: Trouble loading config file {}, reason: {}"
                 .format(arg_config_path, repr(err)))

        # Hard-coded parameter values that might be configured in the future:
        self.n_ints_in_file = get_config_int(config, section, "n_ints_in_file")
        self.dt = get_config_float(config, section, "dt")
        self.df = get_config_float(config, section, "df")
        self.fch1 = get_config_float(config, section, "fch1")
        self.fchans = get_config_int(config, section, "fchans")


if __name__ == "__main__":
    # Unit test debugging
    cfgobj = ConfigObject("spectra_gen.cfg")
    print("\nDump of the config object follows:")
    print(vars(cfgobj))
