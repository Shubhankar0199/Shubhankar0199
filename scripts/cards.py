#!/usr/bin/env python3
import json, html
from pathlib import Path
from github_api import get_repository
ROOT=Path(__file__).resolve().parents[1]
projects=json.loads((ROOT/'data/projects.json').read_text())['projects']

def card(p,theme):
    light=theme=='light'; bg='#ffffff' if light else '#0d1117'; border='#d0d7de' if light else '#30363d'; text='#1f2328' if light else '#c9d1d9'; muted='#656d76' if light else '#8b949e'; green='#1a7f37' if light else '#39d353'
    try: r=get_repository(p['repo']); stars=r.get('stargazers_count',0); forks=r.get('forks_count',0); lang=r.get('language') or '—'
    except Exception: stars=forks='—'; lang='—'
    tech=' • '.join(p['technologies'])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 250"><rect x="4" y="4" width="752" height="242" rx="18" fill="{bg}" stroke="{border}"/><text x="32" y="45" fill="{green}" font-family="ui-monospace,monospace" font-size="20" font-weight="700">◇ {html.escape(p['name'])}</text><text x="32" y="84" fill="{text}" font-family="ui-monospace,monospace" font-size="14">{html.escape(p['description'])[:76]}</text><text x="32" y="108" fill="{text}" font-family="ui-monospace,monospace" font-size="14">{html.escape(p['description'])[76:152]}</text><text x="32" y="155" fill="{muted}" font-family="ui-monospace,monospace" font-size="13">{html.escape(tech)}</text><text x="32" y="202" fill="{muted}" font-family="ui-monospace,monospace" font-size="13">★ {stars}   ⑂ {forks}   ◈ {html.escape(str(lang))}</text></svg>'''
for p in projects:
    key={'Sentiment Analysis System':'sentiment','MedCode AI':'medcode','Resume Analyzer':'resume','AI Assistant v1':'assistant'}[p['name']]
    for theme in ['dark','light']:
        (ROOT/'assets'/f'project-{key}-{theme}.svg').write_text(card(p,theme),encoding='utf-8')
