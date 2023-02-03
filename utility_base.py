
import os
from datetime import datetime
import utils


class BaseSplunkAppUtility:
    def __init__(self, github_action_dir, app_package_dir, main_branch_name) -> None:
        self.GITHUB_ACTION_DIR = github_action_dir
        self.APP_PACKAGE_DIR = app_package_dir

        self.add_utility()
        current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        new_branch = 'splunk_app_utility_change_{}'.format(current_datetime)
        self.create_github_pr(main_branch_name, new_branch)


    def create_github_pr(main_branch, new_branch):
        # checkout main branch
        os.system(r'git checkout {}'.format(main_branch))

        # Create a new branch
        os.system(r'git checkout -b {} {}'.format(new_branch, main_branch))

        # Add app changes
        os.system(r'git add -A')

        # Commit changes
        os.system(r'git commit -m "Splunk App Utility Updated by Github Action."')

        # Push branch on github
        return_value = os.system(r'git push -u origin {}'.format(new_branch))
        if return_value !=0:
            utils.error("Unable to push changes into the branch={}".format(new_branch))
            return

        # Create PR
        os.system(r'gh pr create --base {} --head {} --fill'.format(main_branch, new_branch))
