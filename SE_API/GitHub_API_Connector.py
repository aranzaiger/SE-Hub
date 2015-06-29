__author__ = 'sagi'
import requests


def get_repo_general_info(repo_url):
    url = 'https://api.github.com/repos/' + repo_url
    req = requests.get(url)
    return req.json()


def get_repo_stats(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '/stats/contributors'
    req = requests.get(url)
    return req.json()


def get_repo_issues(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '/issues'
    req = requests.get(url)
    return req.json()


def get_github_data(repo_url):
    project_info = {'stats': None, 'issues': None, 'info': None}

    project_info['stats'] = get_repo_stats(repo_url) #first Call
    project_info['info'] = get_repo_general_info(repo_url)
    project_info['issues'] = get_repo_issues(repo_url)
    project_info['stats'] = get_repo_stats(repo_url) #Second Call

    return project_info