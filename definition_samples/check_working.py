import defconf
import yaml

definition = yaml.load(open('check_testfile.yml') )
config = yaml.load(open('test_1.yml') )
defconf1.validate_config(config, definition, 'test_1.yml')
