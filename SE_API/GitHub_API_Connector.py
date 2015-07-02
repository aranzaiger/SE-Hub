__author__ = 'sagi'
import requests
from GithubAPI.GithubAPI import GitHubAPI_Keys
from models.Task import Task
from google.appengine.ext import db
import datetime

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
    week_obj = {}
    week_obj['data'] = []
    try:
        week_obj['data'].append(req.json()['all'][-4:])
    except:
        week_obj['data'].append([0,0,0,0])

    week_obj['labels'] = []
    # i = 24 * 7 * -1
    # while i != 0:
    #     week_obj['labels'].append((datetime.datetime.today() - datetime.timedelta(hours=i)).strftime("%A"))
    #     i += 24

    week_obj['labels'].append("A Month Ago")
    week_obj['labels'].append("2 Weeks Ago")
    week_obj['labels'].append("1 Weeks Ago")
    week_obj['labels'].append("Most Resent Week")

    return week_obj

def get_repo_commits(repo_url):
    url = 'https://api.github.com/repos/' + repo_url + '/commits' + '?client_id=' + githubKeys.getId() + '&client_secret=' + githubKeys.getSecret()
    req = requests.get(url)
    return req.json()

def make_macro(stats, info, project_id):
    macro = {'labels': [], 'data': [[0]]}
    macro['labels'].append('Commits')
    macro['labels'].append('Open Issues')
    macro['labels'].append('Unfinished Tasks')
    for stat in stats:
        macro['data'][0][0] += stat['total']
    macro['data'][0].append(info['open_issues'])
    macro['data'][0].append(get_unfinished_tasks_number(project_id))

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
        if issue['assignee']:
            if issue['assignee']['login'] == user:
                numOfIssues += 1
    return numOfIssues

def get_github_data(repo_url, project_id):
    project_info = {'stats': {}}
    github_stats =  get_repo_stats(repo_url) #first Call
    project_info['info'] = get_repo_general_info(repo_url)
    issues = get_repo_issues(repo_url)
    weekly_commits  = get_repo_weekly_commits(repo_url)
    github_stats =  get_repo_stats(repo_url) #Second Call
    project_info['stats']['macro'] = make_macro(github_stats, project_info['info'], project_id)
    project_info['stats']['micro'] = make_micro(github_stats, issues)
    project_info['stats']['weekly_commits'] = weekly_commits
    project_info['issues'] = issues
    project_info['commits'] = get_repo_commits(repo_url)

    return project_info


def get_unfinished_tasks_number(project_id):
    # query = Task.all().filter("isPersonal =", False, "")
    return 7