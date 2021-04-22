from github2pandas.utility import Utility
from github2pandas.version import Version
from pathlib import Path
import os

github_token = os.environ['TOKEN']
git_repo_name = os.environ['CI_REPOSITORY_NAME']
git_repo_owner = os.environ['CI_REPOSITORY_OWNER']
    
default_data_folder = Path("data", git_repo_name)

repo = Utility.get_repo(git_repo_owner, git_repo_name, github_token, default_data_folder)

Version.clone_repository(repo=repo, data_root_dir=default_data_folder, github_token=github_token)
Version.generate_version_pandas_tables(data_root_dir=default_data_folder)

print("Aus die Maus!")
