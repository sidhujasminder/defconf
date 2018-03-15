import yaml
import logging
import sys
import pprint
import re

'''
== Reminder of available Exception ==

Exception 	            Base class for all exceptions
StopIteration 	        Raised when the next() method of an iterator does not point to any object.
SystemExit 	            Raised by the sys.exit() function.
StandardError 	        Base class for all built-in exceptions except StopIteration and SystemExit.
ArithmeticError     	Base class for all errors that occur for numeric calculation.
OverflowError 	        Raised when a calculation exceeds maximum limit for a numeric type.
FloatingPointError 	    Raised when a floating point calculation fails.
ZeroDivisonError 	    Raised when division or modulo by zero takes place for all numeric types.
AssertionError 	        Raised in case of failure of the Assert statement.
AttributeError 	        Raised in case of failure of attribute reference or assignment.
EOFError 	            Raised when there is no input from either the raw_input() or input() function and the end of file is reached.
ImportError 	        Raised when an import statement fails.
KeyboardInterrupt 	    Raised when the user interrupts program execution, usually by pressing Ctrl+c.
LookupError 	        Base class for all lookup errors.
IndexError              Raised when an index is not found in a sequence.
KeyError                Raised when the specified key is not found in the dictionary.
NameError 	            Raised when an identifier is not found in the local or global namespace.
UnboundLocalError       Raised when trying to access a local variable in a function or method but no value has been assigned to it.
EnvironmentError        Base class for all exceptions that occur outside the Python environment.
IOError                 Raised when an input/ output operation fails, such as the print statement or the open() function when trying to open a file that does not exist.
IOError                 Raised for operating system-related errors.
SyntaxError             Raised when there is an error in Python syntax.
IndentationError        Raised when indentation is not specified properly.
SystemError 	        Raised when the interpreter finds an internal problem, but when this error is encountered the Python interpreter does not exit.
SystemExit 	            Raised when Python interpreter is quit by using the sys.exit() function. If not handled in the code, causes the interpreter to exit.
ValueError 	            Raised when the built-in function for a data type has the valid type of arguments, but the arguments have invalid values specified.
RuntimeError 	        Raised when a generated error does not fall into any category.
NotImplementedError     Raised when an abstract method that needs to be implemented in an inherited class is not actually implemented.
'''

logger = logging.getLogger('defconf')
logger.setLevel(logging.DEBUG)

# streamhandler = logging.StreamHandler()
# streamhandler.setLevel(logging.DEBUG)
# # logger = logging.getLogger('defconf')
# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# streamhandler.setFormatter(formatter)
# logger.addHandler(streamhandler)

type_list = {}
type_list['string'] = "<type 'str'>"
type_list['integer'] = "<type 'int'>"
type_list['dict'] = "<type 'dict'>"
type_list['bool'] = "<type 'bool'>"
type_list['list'] = "<type 'list'>"

def one_argument(operator_args):

    try:
        possible_val = operator_args.split(',')
        if operator_args is None:
            raise IndexError("Required number of variables not passed for the operator " + possible_val[0])
    except AttributeError:
        raise AttributeError("Node Value is not defined on which operator must be used.")

def two_argument(operator_args):
    try:
        possible_val = operator_args.split(',')
        if len(possible_val) != 2:
            raise IndexError("Required number of variables not passed for the operator " + possible_val[0])
    except AttributeError:
        raise AttributeError("Node Value is not defined on which operator must be used.")

def two_argument_numeric(operator_args):
    try:
        possible_val = operator_args.split(',')
        if len(possible_val) != 2:
            raise IndexError("Required number of variables not passed for the operator " + possible_val[0])
        else:
            float(possible_val[1].strip())

    except AttributeError:
        raise AttributeError("Node Value is not defined on which operator must be used.")

    except ValueError:
        raise ValueError("Value Error found not floatable value")

def three_argument_numeric(operator_args):
    # print operator_args
    # now we need to check if values are floatable
    try:
        possible_val = operator_args.split(',')
        if len(possible_val) != 3:
            raise IndexError("Required number of variables not passed for the operator " + possible_val[0])
        else:
            for i in possible_val[1:]:
                    float(i.strip())
    except AttributeError:
        raise AttributeError("The nodes on which the testcase needs to run should be defined ")
    except ValueError:
        raise ValueError("Values are not floatable, should be floatable")

def two_argument_delta(operator_args):
    try:
        possible_val = operator_args.split(',')

        if len(possible_val) != 2:
            raise IndexError("Required number of variables not passed for the operator " + possible_val[0])
            # Do we need to check if the value that is used by the user is
            # is % or not. Do we need to report it.

    except AttributeError:
        # If there is no comma separated values then this error will throw up
        raise AttributeError("Node Value is not defined on which operator must be used.")

def n_argument_check(operator_args):

    # This function is for operator is-in, not-in which will check
    # if the node value is present in the list of values.
    try:
        possible_val = operator_args.split(',')

        if len(possible_val) == 1:
            raise ValueError
            # Here also can check if the node is present and is of type string.
            # Maybe one good check.
    except AttributeError:
        # If there is no comma separated values then this error will throw up
        raise AttributeError("Node Value is not defined on which operator must be used.")

    except ValueError:
        raise ValueError("THere is no list of values to which the node value must be checked in")


def check_valid_operator(operater_name, operator_value):
    # print operater_name, operator_value
    # print "Now you have the values Get them checking according to the function"

    switcher = {
        "all-same": one_argument,
        "is-equal": two_argument,
        "not-equal": two_argument,
        "exists": one_argument,
        "not-exists": one_argument,
        "contains": two_argument,
        "not-contains": two_argument,
        "is-gt": two_argument_numeric,
        "is-lt": two_argument_numeric,
        "in-range": three_argument_numeric,
        "not-range": three_argument_numeric,
        "no-diff": one_argument,
        "list-not-less": one_argument,
        "list-not-more": one_argument,
        "delta": two_argument_delta,
        "is-in": n_argument_check,
        "not-in": n_argument_check
    }

    switcher[operater_name](operator_value)



def main():

    ## Get CLI arguments
    config_file_name = sys.argv[1]
    definition_file_name = sys.argv[2]

    logger.info('Will load Config "%s" and def "%s"', config_file_name, definition_file_name )

    ## load master definition file
    # master_definition_file = open('definitionfile.def.yml')
    # master_definition = yaml.load(master_definition_file)

    ## load definition file and validate it (to be implemented)
    definition_file = open(definition_file_name)
    definition = yaml.load(definition_file)

    ## load configuration file and validate it
    config_file = open(config_file_name)

    config = yaml.load(config_file)

    try:
        validate_config( config, definition, config_file_name )
        print ' = Configuration file valid = '
        return logger
    except Exception as e:
        logger.error('Configuration file not valid : ' + str(e))

def check_correct_function(test_details, item_name):
    # print "JAMMYBOI"
    # print test_details
    base_item_name = item_name
    for testinfo in test_details:
        operator = [x for x in testinfo if x not in ['err', 'info']]
        item_name = item_name + '.' + operator[0]
        logger.debug('->validate_dict() %s: Checking if this operator values are defined properly ', item_name)
        check_valid_operator(operator[0], testinfo[operator[0]])

        if 'err' in testinfo and 'info' not in testinfo:
            raise ValueError("INFO for the testcase is missing")
        elif 'err' not in testinfo and 'info' in testinfo:
            raise ValueError("ERR for the testcase is missing")
        elif 'err' not in testinfo and 'info' not in testinfo:
            raise ValueError("INFO and ERR both for the testcase is missing")
        item_name = base_item_name


def validate_config( config_file, definition_file, name ):
    validate_dict( config_file, definition_file['validate']['main'], definition_file, 'root')

def validate_dict( config, definition, definition_file, name ):
    global type_list
    logger.debug('->validate_dict() Start for %s ', name )
    # print definition
    # print definition_file

    # print config
    # print definition

    ## Go over all elements of config
    if isinstance(config, list):
        for i in range(len(config)):
            for key, value in config[i].iteritems():
                item_name = name + '.' + key
                # print item_name
                # For each element check if exists in definition unless * is defined
                if not definition.has_key('*') and not definition.has_key(key):
                    raise IndexError("Unable to find " + item_name + " in definition file")
    else:
        for key, value in config.iteritems():
            item_name = name + '.' + key
            # print item_name
            # For each element check if exists in definition unless * is defined
            if not definition.has_key('*') and not definition.has_key(key):
                raise IndexError("Unable to find " + item_name + " in definition file")

    # Check if All mandatory elements are present
    for key, value in definition.iteritems():
        print key, value
        if value.has_key('mandatory') and value['mandatory'] == 1 and not config.has_key(key):
            item_name = name + '.' + key  # This is added to make it more error more easy to see.
            raise IndexError("Mandatory element " + item_name + " has not been found ")

    ######
    ## Check Element content
    ######
    if isinstance(config, list):
        for i in range(len(config)):
            for key, value in config[i].iteritems():

                ## Define name to use for logging and reporting
                ## If needed update the key in case it's *
                item_name = name + '.' + key
                initial_key = key
                if not definition.has_key(key):
                    logger.debug('->validate_dict() Key replace to "*" for %s', item_name )
                    key = '*'

                item_type = type(value)
                logger.debug('->validate_dict() %s Check element content, type is %s ', item_name, str(item_type) )

                ## Check type if type is define
                if definition[key].has_key('type'):
                    logger.debug('->validate_dict() %s: Option "type" found, will check if is %s', item_name, definition[key]['type'] )

                    if str(item_type) == "<type 'dict'>" or str(item_type) == "<type 'list'>" or str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>" or str(item_type) == "<type 'bool'>":
                        # print type_list
                        # print type_list[definition[key]['type']]

                        if type_list[definition[key]['type']] != str(item_type):
                            raise ValueError(item_name +": Type is not valid for '" + item_name + "': expect '" + type_list[definition[key]['type']] + "' found '" + str(item_type))
                    else:
                        raise RuntimeError(item_name + ": Type not supported " + str(item_type))

                ## Check values if define
                if definition[key].has_key('values'):
                    logger.debug('->validate_dict() %s: Option "values" found, will check if is %s', item_name, definition[key]['values'] )

                    do_match = 0
                    for def_value in definition[key]['values']:
                        if str(item_type) == "<type 'list'>":
                            for entry_value in value:
                                if value == def_value:
                                    do_match = 1
                        elif  str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>":
                            if value == def_value:
                                do_match = 1
                        else:
                            raise NotImplementedError("Values option is not supportd with type: " + str(item_type) )

                    if do_match == 0:
                        raise ValueError("Element value is not valid for '" + item_name + "': expect '" + str(definition[key]['values']) + "' found '" + str(value))

                ## Check Regex
                if definition[key].has_key('validate'):
                    logger.debug('->validate_dict() %s: Option "validate" found, will check it', item_name )
                    validate_name = definition[key]['validate']
                    validate_type = ''

                    # check if is a Validate Block or a Regex

                    logger.debug('->validate_dict() %s: Will check search for %s in validate and regex sections', item_name, validate_name )

                    if definition_file['validate'].has_key(validate_name):
                        validate_type = 'block'

                    elif definition_file['regex'].has_key(validate_name):
                        validate_type = 'regex'
                    else:
                        raise AttributeError(item_name + " Option validate: Unable to find '" + definition[key]['validate'] + "'  neither in Validate nor regex section")

                    ## Do the test based on the type
                    if validate_type == 'regex':
                        do_match = 0
                        reg = re.compile(definition_file['regex'][validate_name])

                        if str(item_type) == "<type 'list'>":
                            for entry_value in value:
                                if reg.match( entry_value ):
                                    do_match = 1
                        elif  str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>":
                            if reg.match( value ):
                                do_match = 1
                        else:
                            raise NotImplementedError("Regex option is not supportd with type: " + str(item_type) )

                        if do_match == 0:
                            raise ValueError(item_name + ": Value is not valid, do not match regex '" + validate_name + "' - value(s): " + str(value))

                    elif validate_type == 'block':
                        validate_name = definition[key]['validate']
                        logger.debug('->validate_dict() %s: Will check block %s with %s', item_name, initial_key, validate_name )

                        if isinstance(config, list):
                            # index_iterate in list
                            index_iterate = [i[0] for i in enumerate(config) if 'iterate' in i[1]][0]
                            validate_dict(config[index_command][initial_key], definition_file['validate'][validate_name], definition_file, item_name)
                        else:
                            validate_dict(config[initial_key], definition_file['validate'][validate_name],
                                          definition_file, item_name)

                    else:
                        raise RuntimeError("Unexpected error, should never end here")
    else:
        for key, value in config.iteritems():

            ## Define name to use for logging and reporting
            ## If needed update the key in case it's *
            item_name = name + '.' + key
            initial_key = key
            if not definition.has_key(key):
                logger.debug('->validate_dict() Key replace to "*" for %s', item_name)
                key = '*'

            item_type = type(value)
            logger.debug('->validate_dict() %s Check element content, type is %s ', item_name, str(item_type))

            ## Check type if type is define
            if definition[key].has_key('type'):
                logger.debug('->validate_dict() %s: Option "type" found, will check if is %s', item_name,
                             definition[key]['type'])

                if str(item_type) == "<type 'dict'>" or str(item_type) == "<type 'list'>" or str(
                        item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>" or str(
                        item_type) == "<type 'bool'>":
                    # print type_list
                    # print type_list[definition[key]['type']]

                    if type_list[definition[key]['type']] != str(item_type):
                        raise ValueError(
                            item_name + ": Type is not valid for '" + item_name + "': expect '" + type_list[
                                definition[key]['type']] + "' found '" + str(item_type))
                else:
                    raise RuntimeError(item_name + ": Type not supported " + str(item_type))

            ## check values for test_include if defined or not
            if definition[key].has_key('function'):
                logger.debug('->validate_dict() %s: Option "function" found, will check if all the testcase'
                             ' in test_include are defined %s', item_name,
                         definition[key]['function'])

                ## getting all the possible testcases:
                testlist = config.get('tests_include')
                for testcase in testlist:
                    if testcase not in config:
                        raise ValueError(
                            item_name + ": Following Testcase is not defined ' " + testcase + " '")

            if definition[key].has_key('function1'):
                logger.debug('->validate_dict() %s: Option "function1" found, will check for if the operators '
                             ' are defined properly in %s', item_name,
                             definition[key]['function1'])
                # print "JAMMY NOW CHEK IF THE OPERATOR ARE CORRECT OR NOT"
                # print config.get('tests')
                check_correct_function(config.get('tests'), item_name)




            ## Check values if define
            if definition[key].has_key('values'):
                logger.debug('->validate_dict() %s: Option "values" found, will check if is %s', item_name,
                             definition[key]['values'])

                do_match = 0
                for def_value in definition[key]['values']:
                    if str(item_type) == "<type 'list'>":
                        for entry_value in value:
                            if value == def_value:
                                do_match = 1
                    elif str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>":
                        if value == def_value:
                            do_match = 1
                    else:
                        raise NotImplementedError("Values option is not supportd with type: " + str(item_type))

                if do_match == 0:
                    raise ValueError("Element value is not valid for '" + item_name + "': expect '" + str(
                        definition[key]['values']) + "' found '" + str(value))

            ## Check Regex
            if definition[key].has_key('validate'):
                logger.debug('->validate_dict() %s: Option "validate" found, will check it', item_name)
                validate_name = definition[key]['validate']
                validate_type = ''

                # check if is a Validate Block or a Regex

                logger.debug('->validate_dict() %s: Will check search for %s in validate and regex sections', item_name,
                             validate_name)

                if definition_file['validate'].has_key(validate_name):
                    validate_type = 'block'

                elif definition_file['regex'].has_key(validate_name):
                    validate_type = 'regex'
                else:
                    raise AttributeError(item_name + " Option validate: Unable to find '" + definition[key][
                        'validate'] + "'  neither in Validate nor regex section")

                ## Do the test based on the type
                if validate_type == 'regex':
                    do_match = 0
                    reg = re.compile(definition_file['regex'][validate_name])

                    if str(item_type) == "<type 'list'>":
                        for entry_value in value:
                            if reg.match(entry_value):
                                do_match = 1
                    elif str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>":
                        if reg.match(value):
                            do_match = 1
                    else:
                        raise NotImplementedError("Regex option is not supportd with type: " + str(item_type))

                    if do_match == 0:
                        raise ValueError(
                            item_name + ": Value is not valid, do not match regex '" + validate_name + "' - value(s): " + str(
                                value))

                elif validate_type == 'block':
                    validate_name = definition[key]['validate']
                    logger.debug('->validate_dict() %s: Will check block %s with %s', item_name, initial_key,
                                 validate_name)

                    validate_dict(config[initial_key], definition_file['validate'][validate_name], definition_file,
                                  item_name)

                else:
                    raise RuntimeError("Unexpected error, should never end here")

    ############
    ## Add default value if not define
    #############
    for key, value in definition.iteritems():
        if value.has_key('default') and not config.has_key(key):
            item_name = name + '.' + key
            logger.debug('->validate_dict() %s: Default value missing', item_name )
            config[key] = value['default']

if __name__ == '__main__':

    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
    main()

