import os
import sys
sys.path.append(os.path.dirname(__file__))

import utils
from utility_logger import LoggerUtility


GITHUB_ACTION_DIR = os.path.dirname(os.path.abspath(__file__))


# This is just for testing
utils.info("Files under current working directory:- {}".format(os.getcwd()))
utils.list_files(os.path.dirname(os.path.dirname(os.getcwd())))


def main(local_test=False):
    app_dir = utils.get_input('app_dir')
    utils.info("app_dir: {}".format(app_dir))

    main_branch_name = utils.get_input('main_branch_name')
    utils.info("main_branch_name: {}".format(main_branch_name))

    app_package_dir = os.path.join('repodir', app_dir)


    utilities_to_add = utils.get_input('utilities_to_add')
    utils.info("utilities_to_add: {}".format(utilities_to_add))


    utilities = utilities_to_add.split(',')
    utilities = [u.strip() for u in utilities]

    for utility in utilities:
        if utility == "logger":
            LoggerUtility(GITHUB_ACTION_DIR, app_package_dir, main_branch_name, local_test=local_test)
        else:
            utils.error("utility={} is not supported.".format(utility))



def perform_local_test(utility_to_test):
    utils.test_set_input('app_dir', 'test_app1')
    utils.test_set_input('main_branch_name', 'main')
    utils.test_set_input('utilities_to_add', utility_to_test)

    # setting other variables for testing
    utilities = utility_to_test.split(',')
    utilities = [u.strip() for u in utilities]

    if 'logger' in utilities:
        utils.test_set_input('logger_sourcetype', 'test:app1:logs')
        utils.test_set_input('log_files_prefix', 'test_app1')

    main(local_test=True)



main()

# perform_local_test(utility_to_test='logger')
