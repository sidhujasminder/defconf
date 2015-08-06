import unittest
import yaml
import sys
import logging
from os import path

import defconf

here = path.abspath(path.dirname(__file__))

class Test_Validate_Main_Block(unittest.TestCase):
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)


    def test_all_good(self):
        files_name = '01_all_good'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        defconf.validate_config( config, definition, files_name )
        self.assertTrue(1)

    def test_missing_mandatory_element(self):
        files_name = '01_missing_mandatory_element'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(IndexError):
            defconf.validate_config( config, definition, files_name )

    def test_undefined_element(self):
        files_name = '02_undefined_element'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(IndexError):
            defconf.validate_config( config, definition, files_name )

    def test_undefined_element_accept_all(self):
        files_name = '02_undefined_element_accept_all'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        defconf.validate_config( config, definition, files_name )
        self.assertTrue(1)

    def test_unvalid_type_str(self):
        files_name = '03_unvalid_type'
        definition = yaml.load( open(path.join(here, 'input', files_name + '_str.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(ValueError):
            defconf.validate_config( config, definition, files_name )

    def test_unvalid_type_list(self):
        files_name = '03_unvalid_type'
        definition = yaml.load( open(path.join(here, 'input', files_name + '_list.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(ValueError):
            defconf.validate_config( config, definition, files_name )

    def test_unvalid_type_dict(self):
        files_name = '03_unvalid_type'
        definition = yaml.load( open(path.join(here, 'input', files_name + '_dict.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(ValueError):
            defconf.validate_config( config, definition, files_name )

    def test_unvalid_type_int(self):
        files_name = '03_unvalid_type'
        definition = yaml.load( open(path.join(here, 'input', files_name + '_int.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(ValueError):
            defconf.validate_config( config, definition, files_name )

    def test_incorrect_values_str(self):
        files_name = '04_incorrect_values_str'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(ValueError):
            defconf.validate_config( config, definition, files_name )

    def test_incorrect_values_list(self):
        files_name = '04_incorrect_values_list'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        with self.assertRaises(ValueError):
            defconf.validate_config( config, definition, files_name )

    def test_default_values(self):
        files_name = '06_default_values'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        defconf.validate_config( config, definition, files_name )

        ##
        self.assertTrue( config.has_key('mail_servers_ports') )
        self.assertTrue( config['mail_servers_ports'] == 25 )

        self.assertTrue( config['database'].has_key('login') )
        self.assertTrue( config['database']['login'] == 'admin' )

    def test_nested_dict_wit_star(self):
        files_name = '07_nested_dict_with_star'
        definition = yaml.load( open(path.join(here, 'input', files_name + '.def.yml')) )
        config = yaml.load( open(path.join(here, 'input', files_name + '.yml')) )

        defconf.validate_config( config, definition, files_name )
        ##
        self.assertTrue( 1 )

def main():
    unittest.main()

if __name__ == '__main__':
    main()
