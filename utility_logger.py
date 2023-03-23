import os
import utils
from utility_base import BaseSplunkAppUtility
import file_handlers


class LoggerUtility(BaseSplunkAppUtility):

    def get_file_to_generate_hash(self):
        return os.path.join(self.GITHUB_ACTION_DIR, 'logger', 'logger_manager.py')


    def add_utility(self):
        log_files_prefix = utils.get_input('log_files_prefix')
        utils.info("log_files_prefix: {}".format(log_files_prefix))
        
        logger_sourcetype = utils.get_input('logger_sourcetype')
        utils.info("logger_sourcetype: {}".format(logger_sourcetype))

        self.words_for_replacement = {
            '<<<log_files_prefix>>>': log_files_prefix,
            '<<<logger_sourcetype>>>': logger_sourcetype
        }

        update1 = self.add_logger_manager_py()
        update2 = self.add_props_content()
        if update1 or update2:
            return True
        return False


    def add_logger_manager_py(self):
        return file_handlers.RawFileHandler(
            os.path.join(self.GITHUB_ACTION_DIR, 'logger', 'logger_manager.py'),
            os.path.join(self.APP_PACKAGE_DIR, 'bin', 'logger_manager.py'),
            self.words_for_replacement
        ).validate_file_content()


    def add_props_content(self):
        return file_handlers.ConfigFileHandler(
            os.path.join(self.GITHUB_ACTION_DIR, 'logger', 'props.conf'),
            os.path.join(self.APP_PACKAGE_DIR, 'default', 'props.conf'),
            self.words_for_replacement
        ).validate_config()
