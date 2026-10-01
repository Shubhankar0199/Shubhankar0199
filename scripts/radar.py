#!/usr/bin/env python3
import json, math, os
from pathlib import Path
from github_api import get_stats

ROOT=Path(__file__).resolve().parents[1]
SELF=json.loads((ROOT/'data/skills.json').read_text())['self_assessed']

def svg(title, labels, values, filename, color='#39d353'):
    w=h=520; cx=260; cy=270; R=175; n=len(labels)
    pts=[]; axes=[]; texts=[]
    for i,(lab,val) in enumerate(zip(labels,values)):
        ang=-math.pi/2+i*2*math.pi/n
        x=cx+R*math.cos(ang); y=cy+R*math.sin(ang); axes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')
        tx=cx+(R+34)*math.cos(ang); ty=cy+(R+34)*math.sin(ang)+4
        anchor='middle' if abs(math.cos(ang))<.5 else ('start' if math.cos(ang)>0 else 'end')
        texts.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{lab}</text>')
        pr=R*val/100; pts.append(f'{cx+pr*math.cos(ang):.1f},{cy+pr*math.sin(ang):.1f}')
    grids=[]
    for level in [20,40,60,80,100]:
        gp=[]
        for i in range(n):
            ang=-math.pi/2+i*2*math.pi/n; gp.append(f'{cx+R*level/100*math.cos(ang):.1f},{cy+R*level/100*math.sin(ang):.1f}')
        grids.append(f'<polygon points="{" ".join(gp)}"/>')
    body=''.join(f'<text x="260" y="34" text-anchor="middle" class="title">{title}</text>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;fill:#c9d1d9;font-size:12px}}.title{{font-size:16px;font-weight:700}}.grid,.axis{{fill:none;stroke:#30363d;stroke-width:1}}.area{{fill:{color};fill-opacity:.16;stroke:{color};stroke-width:2}}</style><rect width="100%" height="100%" rx="18" fill="#0d1117"/>{body}<g class="grid">{''.join(grids)}</g><g class="axis">{''.join(axes)}</g><polygon class="area" points="{' '.join(pts)}"/>{''.join(texts)}</svg>'''
    (ROOT/'assets'/filename).write_text(svg,encoding='utf-8')

svg('Self-assessed skill areas',list(SELF),list(SELF.values()),'radar-dark.svg')
# light theme
svg('Self-assessed skill areas',list(SELF),list(SELF.values()),'radar-light.svg',color='#1a7f37')
try:
    stats=get_stats(); langs=stats['languages']; top=sorted(langs.items(),key=lambda x:x[1],reverse=True)[:8]
    if top:
        labels=[x[0] for x in top]; vals=[round(100*v/top[0][1]) for v in top]
        svg('GitHub language usage (relative)',labels,vals,'radar-languages-dark.svg')
        svg('GitHub language usage (relative)',labels,vals,'radar-languages-light.svg',color='#1a7f37')
except Exception as e:
    # Never invent language percentages. Keep an explicit generated placeholder.
    for f in ['radar-languages-dark.svg','radar-languages-light.svg']:
        light='light' in f
        bg='#ffffff' if light else '#0d1117'; fg='#1f2328' if light else '#c9d1d9'
        Path(ROOT/'assets'/f).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 300"><rect width="100%" height="100%" rx="18" fill="{bg}"/><text x="260" y="135" text-anchor="middle" fill="{fg}" font-family="monospace" font-size="16">GitHub language data</text><text x="260" y="165" text-anchor="middle" fill="{fg}" font-family="monospace" font-size="12">Run radar.yml to refresh</text></svg>')
