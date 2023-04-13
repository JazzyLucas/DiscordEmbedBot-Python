import configparser

# Read the config file
config = configparser.ConfigParser(interpolation=None)
config.read('config.txt')

# Iterate over sections and options to censor all values
for section in config.sections():
    for option in config.options(section):
        censored_parts = []
        for part in config.get(section, option).split('.'):
            censored_part = '*' * (len(part))
            censored_parts.append(censored_part)
        censored_value = '.'.join(censored_parts)
        config.set(section, option, censored_value)

# Write the sample config and uppercase it
with open('SAMPLEconfig.txt', 'w') as f:
    config.write(f)

with open('SAMPLEconfig.txt', 'r') as f:
    content = f.read().upper()

with open('SAMPLEconfig.txt', 'w') as f:
    f.write(content)