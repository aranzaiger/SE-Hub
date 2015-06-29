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

def get_repo_weekly_commits(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '/stats/participation' + '?client_id=' + githubKeys.getId() + '&client_secret=' + githubKeys.getSecret()
    req = requests.get(url)
    try:
        return req.json()['all']
    except:
        return []

def make_macro(stats, info):
    macro = {'labels': [], 'data': [[0]]}
    macro['labels'].append('Commits')
    macro['labels'].append('Open Issues')
    for stat in stats:
        macro['data'][0][0] += stat['total']
    macro['data'][0].append(info['open_issues'])

    return macro

def make_micro(stats, issues):
    micro = {'labels': [], 'data': [], 'series': []}
    micro['labels'].append('Commits')
    micro['labels'].append('Open Issues')
    for stat in stats:
        micro['series'].append(stat['author']['login'])
        micro['data'].append([stat['total'], get_issue_num(issues, stat['author']['login'])])

    return micro

def get_issue_num(issues, user):
    numOfIssues = 0
    for issue in issues:
        if issue['user']['login'] == user:
            numOfIssues += 1
    return numOfIssues

def get_github_data(repo_url):
    project_info = {'stats': {}}
    github_stats =  get_repo_stats(repo_url) #first Call
    project_info['info'] = get_repo_general_info(repo_url)
    issues = get_repo_issues(repo_url)
    weekly_commits  = get_repo_weekly_commits(repo_url)
    github_stats =  get_repo_stats(repo_url) #Second Call
    project_info['stats']['macro'] = make_macro(github_stats, project_info['info'])
    project_info['stats']['micro'] = make_micro(github_stats, issues)
    project_info['stats']['weekly_commits'] = weekly_commits
    project_info['issues'] = issues

    return project_info
