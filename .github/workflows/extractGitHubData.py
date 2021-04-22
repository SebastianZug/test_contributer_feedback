from github2pandas.utility import Utility
from pathlib import Path
import os

github_token = os.environ['TOKEN']
git_repo_name = os.environ['CI_REPOSITORY_NAME']
git_repo_owner = os.environ['CI_REPOSITORY_OWNER']
    
default_data_folder = Path("data", git_repo_name)

repo = Utility.get_repo(git_repo_owner, git_repo_name, github_token, default_data_folder)
print("Aus die Maus!")
