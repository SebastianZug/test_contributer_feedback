from github2pandas.utility import Utility
from github2pandas.version import Version
from pathlib import Path
import os
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

github_token = os.environ['TOKEN']
git_repo_name = os.environ['CI_REPOSITORY_NAME']
git_repo_owner = os.environ['CI_REPOSITORY_OWNER']
    
default_data_folder = Path("data", git_repo_name)

def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
    leadingText = originalText.split(delimeterA)[0]
    trailingText = originalText.split(delimterB)[1]
    return leadingText + delimeterA + replacementText + delimterB + trailingText

def getDataToPlot(df, author):
    data = df.copy()
    data = data[data.author==author]
    data['day'] = pd.to_datetime(data['commited_at'])
    data.set_index('day', inplace=True)
    result = data.groupby(pd.Grouper(freq='D')).sum()
    result['lines_sum'] = result.total_added_lines.cumsum().astype('int64')
    return result

if __name__ == "__main__":
    repo = Utility.get_repo(git_repo_owner, git_repo_name, github_token, default_data_folder)
    Version.clone_repository(repo=repo, data_root_dir=default_data_folder, github_token=github_token)
    Version.no_of_proceses = 8
    Version.generate_version_pandas_tables(repo = repo, data_root_dir=default_data_folder)
    
    users = Utility.get_users(default_data_folder)
    pdCommits = Version.get_version(data_root_dir=default_data_folder)
    pdEdits = Version.get_version(data_root_dir=default_data_folder, filename=Version.VERSION_EDITS)

    pdEdits = pdEdits.merge(pdCommits[['commit_sha', 'author', 'commited_at']], left_on='commit_sha', right_on='commit_sha')
    pdFileEdits = pdEdits.groupby(['commit_sha']).first()
    counts = pdFileEdits.groupby(['author']).agg({'total_added_lines': 'sum', 'total_removed_lines': 'sum'})
    
    # Generate Table 
    # todo
        
    # Generate Figure 
    fig, ax = plt.subplots()
    filename = "AddedlinesOfCode"
    for user in users.anonym_uuid.values:
        df = getDataToPlot(pdFileEdits, user)
        df.lines_sum.plot(drawstyle="steps-mid", linewidth = 2, ax = ax)

    ax.legend(users.anonym_uuid.values)
    ax.set_xlabel("Date")
    ax.set_ylabel('Added Lines of Code')
    plt.tight_layout()
    fig.savefig(filename+".png")
    print("File saved to " + filename + ".png")
