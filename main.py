import os
import sys
sys.path.append(os.path.dirname(__file__))

import utils
from utility_logger import LoggerUtility


GITHUB_ACTION_DIR = os.path.dirname(os.path.abspath(__file__))


app_dir = utils.get_input('app_dir')
utils.info("app_dir: {}".format(app_dir))

main_branch_name = utils.get_input('main_branch_name')
utils.info("main_branch_name: {}".format(main_branch_name))

APP_PACKAGE_DIR = os.path.join('repodir', app_dir)


utilities_to_add = utils.get_input('utilities_to_add')
utils.info("utilities_to_add: {}".format(utilities_to_add))


# This is just for testing
utils.info("Files under current working directory:- {}".format(os.getcwd()))
# utils.list_files(os.getcwd())



def main(local_test=False):
    utilities = utilities_to_add.split(',')
    utilities = [u.strip() for u in utilities]

    for utility in utilities:
        if utility == "logger":
            LoggerUtility(GITHUB_ACTION_DIR, APP_PACKAGE_DIR, main_branch_name, local_test=local_test)
        else:
            utils.error("utility={} is not supported.".format(utility))



def perform_local_test(test_utilities):
    global app_dir
    app_dir = 'test_app1'
    utils.info("TEST - app_dir: {}".format(app_dir))

    global main_branch_name
    main_branch_name = 'main'
    utils.info("TEST - main_branch_name: {}".format(main_branch_name))

    global APP_PACKAGE_DIR
    APP_PACKAGE_DIR = os.path.join('repodir', app_dir)

    global utilities_to_add
    utilities_to_add = test_utilities
    utils.info("TEST - utilities_to_add: {}".format(utilities_to_add))

    utilities = utilities_to_add.split(',')
    utilities = [u.strip() for u in utilities]

    if 'logger' in utilities:
        utils.set_env('logger_sourcetype', 'test:app1:logs')
        utils.set_env('log_files_prefix', 'test_app1')

    main()



# main()

perform_local_test(utilities_to_add='')
