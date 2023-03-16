import os
import utils
from utility_base import BaseSplunkAppUtility
import file_handlers


class CommonSplunkJSUtility(BaseSplunkAppUtility):

    def get_file_to_generate_hash(self):
        return os.path.join(self.GITHUB_ACTION_DIR, 'common_splunk_js_utilities', 'splunk_common_js_v_utilities.js')

    def add_utility(self):
        file_handlers.RawFileHandler(
            os.path.join(self.GITHUB_ACTION_DIR, 'common_splunk_js_utilities', 'splunk_common_js_v_utilities.js'),
            os.path.join(self.APP_PACKAGE_DIR, 'appserver', 'static', 'splunk_common_js_v_utilities.js')
        ).validate_file_content()
