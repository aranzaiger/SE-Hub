__author__ = 'sagi'
import requests
from GithubAPI.GithubAPI import GitHubAPI_Keys

githubKeys = GitHubAPI_Keys()

def get_repo_general_info(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '?client_id='+githubKeys.getId()+'&client_secret=' + githubKeys.getSecret()
    req = requests.get(url)
    return req.json()


def get_repo_stats(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '/stats/contributors' + '?client_id='+githubKeys.getId()+'&client_secret=' + githubKeys.getSecret()
    req = requests.get(url)
    return req.json()


def get_repo_issues(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '/issues' + '?client_id=' + githubKeys.getId() + '&client_secret=' + githubKeys.getSecret()
    req = requests.get(url)
    return req.json()


def get_github_data(repo_url):
    project_info = {'stats': None, 'issues': None, 'info': None}

    project_info['stats'] = get_repo_stats(repo_url) #first Call
    project_info['info'] = get_repo_general_info(repo_url)
    project_info['issues'] = get_repo_issues(repo_url)
    project_info['stats'] = get_repo_stats(repo_url) #Second Call

    return project_info