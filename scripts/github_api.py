#!/usr/bin/env python3
import os, requests
from collections import Counter

USERNAME=os.getenv('GITHUB_USERNAME','Shubhankar0199')
BASE='https://api.github.com'

def _session():
    s=requests.Session(); s.headers.update({'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    token=os.getenv('GITHUB_TOKEN') or os.getenv('METRICS_TOKEN')
    if token: s.headers['Authorization']=f'Bearer {token}'
    return s

def _get(path, params=None):
    r=_session().get(BASE+path,params=params,timeout=30); r.raise_for_status(); return r.json()

def get_user(): return _get(f'/users/{USERNAME}')
def get_repositories():
    repos=[]; page=1
    while True:
        batch=_get(f'/users/{USERNAME}/repos',{'per_page':100,'page':page,'type':'owner','sort':'updated'})
        repos.extend(batch)
        if len(batch)<100: return repos
        page+=1

def get_repository(repo): return _get(f'/repos/{repo}')
def get_languages(repo): return _get(f'/repos/{repo}/languages')
def get_stats():
    user=get_user(); repos=get_repositories()
    languages=Counter()
    for r in repos:
        try: languages.update(get_languages(r['full_name']))
        except requests.HTTPError: pass
    return {'repositories':user.get('public_repos',0),'followers':user.get('followers',0),'following':user.get('following',0),'stars':sum(r.get('stargazers_count',0) for r in repos),'forks':sum(r.get('forks_count',0) for r in repos),'languages':dict(languages)}

def get_contributions():
    # GitHub's contribution calendar is GraphQL-only; use the GraphQL endpoint when a token is available.
    token=os.getenv('GITHUB_TOKEN') or os.getenv('METRICS_TOKEN')
    if not token: raise RuntimeError('GITHUB_TOKEN or METRICS_TOKEN is required for contribution data')
    query='''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'''
    r=requests.post('https://api.github.com/graphql',json={'query':query,'variables':{'login':USERNAME}},headers={'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json'},timeout=30); r.raise_for_status(); return r.json()['data']['user']['contributionsCollection']
