from github import Github
import yaml
import os

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()

os.environ['GITHUB_TOKEN'] = config['github']['token']
token = os.getenv('GITHUB_TOKEN')
g = Github(token)

# Function to search for a YAML file in a public repository and look for a token
def search_for_token_in_public_repo(user_name, repo_name, file_name='config.yaml'):
    try:
        repo = g.get_repo(f"{user_name}/{repo_name}")
        if repo.private:
            print(f"Repository '{repo_name}' is private. Cannot search for tokens.")
            return

        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.type == "file" and file_content.name == file_name:
                print(f"Found '{file_name}' in repository '{repo_name}'.")
                file_data = file_content.decoded_content.decode('utf-8')
                
                # Parse the YAML data
                yaml_data = yaml.safe_load(file_data)
                token = yaml_data.get('github', {}).get('token')
                if token:
                    print(f"Token found: {token}")
                else:
                    print(f"No token found in '{file_name}'.")
                return
        
        print(f"File '{file_name}' not found in repository '{repo_name}'.")
    except Exception as e:
        print(f"Error searching repository '{repo_name}': {e}")

# Demonstrate the risk of misconfiguring by searching for a token in a public repository
public_user = "DolevGabay"
public_repo = "varonis"
search_for_token_in_public_repo(public_user, public_repo)
