
import os
import utils


class BaseSplunkAppUtility:
    def __init__(self, github_action_dir, repo_dir, app_package_dir, main_branch_name, local_test=False) -> None:
        self.GITHUB_ACTION_DIR = github_action_dir
        self.REPO_DIR = repo_dir
        self.APP_PACKAGE_DIR = app_package_dir

        self.add_utility()
        _hash = utils.get_file_hash(self.get_file_to_generate_hash())
        new_branch = 'splunk_app_utility_change_{}_{}'.format(self.__class__.__name__, _hash)
        utils.info("Branch Name: {}".format(new_branch))
        if not local_test:
            os.chdir(self.REPO_DIR)
            if self.check_branch_does_not_exist(new_branch):
                self.configure_git()
                self.create_github_pr(main_branch_name, new_branch)
            else:
                utils.info("Branch already present.")


    def check_branch_does_not_exist(self, branch_name):
        # https://stackoverflow.com/questions/5167957/is-there-a-better-way-to-find-out-if-a-local-git-branch-exists
        os.system('git fetch')
        utils.info("Checking whether git branch already present or not.")
        # ret_code = os.system('git rev-parse --verify {}'.format(branch_name))
        ret_code = os.system('git checkout {}'.format(branch_name))
        if ret_code != 0:
            return True
        return False


    def configure_git(self):
        if not os.environ.get("GITHUB_TOKEN"):
            raise ValueError("Please configure the GitHub Token in GH_TOKEN environment secret for actions in the Repo Settings.")

        os.system(r'gh auth setup-git')
        os.system(r'git config user.name SplunkAppUtilityAction')
        os.system(r'git config user.email splunkapputilityaction@crossrealms.com')


    def create_github_pr(self, main_branch, new_branch):
        utils.info("Committing the code and creating PR.")
        # checkout main branch
        os.system(r'git checkout {}'.format(main_branch))

        # Create a new branch
        os.system(r'git checkout -b {} {}'.format(new_branch, main_branch))

        # Add app changes
        os.system(r'git add -A')

        # Commit changes
        os.system(r'git commit -m "{}"'.format(new_branch))

        # Push branch on github
        return_value = os.system(r'git push -u origin {}'.format(new_branch))
        if return_value !=0:
            utils.error("Unable to push changes into the branch={}".format(new_branch))
            return

        # Create PR
        os.system(r'gh pr create --base {} --head {} --fill'.format(main_branch, new_branch))
