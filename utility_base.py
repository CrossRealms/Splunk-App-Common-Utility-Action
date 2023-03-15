
import os
import utils


class BaseSplunkAppUtility:
    def __init__(self, github_action_dir, app_package_dir, main_branch_name, local_test=False) -> None:
        self.GITHUB_ACTION_DIR = github_action_dir
        self.APP_PACKAGE_DIR = app_package_dir

        self.add_utility()
        _hash = utils.get_file_hash(self.get_file_to_generate_hash())
        new_branch = 'splunk_app_utility_change_{}_'.format(__class__.__name__, _hash)
        if not local_test:
            if self.check_branch_does_not_exist(new_branch):
                self.create_github_pr(main_branch_name, new_branch)
            else:
                utils.info("Branch already present.")


    def check_branch_does_not_exist(self, branch_name):
        # https://stackoverflow.com/questions/5167957/is-there-a-better-way-to-find-out-if-a-local-git-branch-exists
        return True


    def create_github_pr(self, main_branch, new_branch):
        # checkout main branch
        os.system(r'git checkout {}'.format(main_branch))

        # Create a new branch
        os.system(r'git checkout -b {} {}'.format(new_branch, main_branch))

        # Add app changes
        os.system(r'git add -A')

        # Commit changes
        os.system(r'git commit -m "Splunk App Utility Updated by Github Action ({})"'.format(new_branch))

        # Push branch on github
        return_value = os.system(r'git push -u origin {}'.format(new_branch))
        if return_value !=0:
            utils.error("Unable to push changes into the branch={}".format(new_branch))
            return

        # Create PR
        os.system(r'gh pr create --base {} --head {} --fill'.format(main_branch, new_branch))
