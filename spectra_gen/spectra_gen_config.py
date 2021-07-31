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
    try:
        parm_value = arg_config[arg_section][arg_key]
    except KeyError:
        oops("Key not found in config file section {} key {}"
             .format(arg_section, arg_key))        
    except Exception as err:
        oops("get_config_string: config file section {} key {}, reason: {}"
             .format(arg_section, arg_key, repr(err)))
    print("get_config_string: {} = {}".format(arg_key, parm_value))
    return parm_value


def get_config_boolean(arg_config, arg_section, arg_key):
    """
    get one BOOLEAN configuration parameter by key
    """
    try:
        parm_value = bool(arg_config[arg_section][arg_key])
    except KeyError:
        oops("Key not found in config file section {} key {}"
             .format(arg_section, arg_key))        
    except Exception as err:
        oops("get_config_boolean: config file section {} key {}, reason: {}"
             .format(arg_section, arg_key, repr(err)))
    print("get_config_boolean: {} = {}".format(arg_key, parm_value))
    return parm_value


def get_config_int(arg_config, arg_section, arg_key, ):
    """
    get one INTEGER configuration parameter by key
    """
    try:
        parm_value = int(arg_config[arg_section][arg_key])
    except KeyError:
        oops("Key not found in config file section {} key {}"
             .format(arg_section, arg_key))        
    except Exception as err:
        oops("get_config_int: config file section {} key {}, reason: {}"
             .format(arg_section, arg_key, repr(err)))
    print("get_config_int: {} = {}".format(arg_key, parm_value))
    return parm_value


def get_config_float(arg_config, arg_section, arg_key):
    """
    get one FLOAT configuration parameter by key
    """
    try:
        parm_value = float(arg_config[arg_section][arg_key])
    except KeyError:
        oops("Key not found in config file section {} key {}"
             .format(arg_section, arg_key))        
    except Exception as err:
        oops("get_config_float: config file section {} key {}, reason: {}"
             .format(arg_section, arg_key, repr(err)))
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
            print("get_config_all: config file {} was loaded"
                   .format(arg_config_path))
        except Exception as err:
            oops("get_config: Trouble loading config file {}, reason: {}"
                 .format(arg_config_path, repr(err)))

        # Main section
        self.n_ints_in_file = get_config_int(config, "main", "n_ints_in_file")
        self.dt = get_config_float(config, "main", "dt")
        self.df = get_config_float(config, "main", "df")
        self.fch1 = get_config_float(config, "main", "fch1")
        self.n_fine_chans = get_config_int(config, "main", "n_fine_chans")
        self.ascending = get_config_boolean(config, "main", "ascending")
        self.adding_noise = get_config_boolean(config, "main", "adding_noise")
        if self.adding_noise:
            self.noise_x_mean = get_config_float(config, "main", "noise_x_mean")

        # Signal 1
        self.signal_start_1 = get_config_float(config, "signal_1", "signal_start_1")
        self.drift_rate_1 = get_config_float(config, "signal_1", "drift_rate_1")
        self.width_1 = get_config_float(config, "signal_1", "width_1")
        self.snr_1 = get_config_float(config, "signal_1", "snr_1")
        self.f_profile_type_1 = get_config_string(config, "signal_1", "f_profile_type_1")

        # Signal 2
        self.signal_start_2 = get_config_float(config, "signal_2", "signal_start_2")
        self.drift_rate_2 = get_config_float(config, "signal_2", "drift_rate_2")
        self.width_2 = get_config_float(config, "signal_2", "width_2")
        self.snr_2 = get_config_float(config, "signal_2", "snr_2")
        self.f_profile_type_2 = get_config_string(config, "signal_2", "f_profile_type_2")

        # Signal 3
        self.signal_start_3 = get_config_float(config, "signal_3", "signal_start_3")
        self.drift_rate_3 = get_config_float(config, "signal_3", "drift_rate_3")
        self.width_3 = get_config_float(config, "signal_3", "width_3")
        self.snr_3 = get_config_float(config, "signal_3", "snr_3")
        self.f_profile_type_3 = get_config_string(config, "signal_3", "f_profile_type_3")


if __name__ == "__main__":
    # Unit test debugging
    cfgobj = ConfigObject("spectra_gen.cfg")
    print("\nDump of the config object follows:")
    print(vars(cfgobj))
