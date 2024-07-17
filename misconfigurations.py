import os
import yaml
from github import Github

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()

os.environ['GITHUB_TOKEN'] = config['github']['token']
token = os.getenv('GITHUB_TOKEN')
g = Github(token)

# Function to check and fix repository visibility
def check_and_fix_repo_visibility(user_name, repo_name):
    user = g.get_user(user_name)
    repo = user.get_repo(repo_name)

    if repo.private:
        print(f"Repository '{repo_name}' is private.")
    else:
        print(f"Repository '{repo_name}' is public. Changing it to private.")
        repo.edit(private=True)
        print(f"Repository '{repo_name}' is now private.")

# Function to check and fix branch protection rules
def check_and_fix_branch_protection(user_name, repo_name, branch_name):
    user = g.get_user(user_name)
    repo = user.get_repo(repo_name)
    branch = repo.get_branch(branch_name)

    try:
        protection = branch.get_protection()
        print(f"Branch '{branch_name}' has protection rules.")
    except:
        print(f"Branch '{branch_name}' does not have protection rules. Adding protection rules.")
        repo.get_branch(branch_name).edit_protection(
            required_approving_review_count=1,  # At least one review is required to approve a pull request
            enforce_admins=True,                # Admins must also follow these rules
            require_code_owner_reviews=True     # At least one review must come from a code owner
        )
        print(f"Protection rules added to branch '{branch_name}'.")

# Function to check and add an SSH key to the authenticated user's GitHub account
def check_and_add_ssh_key(ssh_key_title, ssh_key_path):
    user = g.get_user()
    keys = user.get_keys()

    with open(os.path.expanduser(ssh_key_path), 'r') as key_file:
        ssh_key = key_file.read().strip()

    for key in keys:
        if key.title == ssh_key_title:
            print(f"SSH key '{ssh_key_title}' is already added to user '{user.login}'.")
            return

    user.create_key(title=ssh_key_title, key=ssh_key)
    print(f"SSH key '{ssh_key_title}' has been added to user '{user.login}'.")

def main():
    check_and_fix_repo_visibility(config['github']['username'], config['github']['repo_visibility'])
    check_and_fix_branch_protection(config['github']['username'], config['github']['repo_protection'], config['github']['branch'])
    check_and_add_ssh_key(config['github']['ssh_key_title'], config['github']['ssh_key_path'])

if __name__ == "__main__":
    main()
