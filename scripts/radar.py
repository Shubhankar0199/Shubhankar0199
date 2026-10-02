#!/usr/bin/env python3
import json, math
from html import escape
from pathlib import Path
from github_api import get_stats

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
SELF = json.loads((ROOT / 'data/skills.json').read_text())['self_assessed']

THEMES = {
    'dark':  dict(bg='#0d1117', fg='#c9d1d9', line='#30363d', accent='#39d353'),
    'light': dict(bg='#ffffff', fg='#1f2328', line='#d0d7de', accent='#1a7f37'),
}


def radar(title, labels, values, filename, theme):
    t = THEMES[theme]
    w, h, cx, cy, R = 640, 540, 320, 280, 175
    n = len(labels)
    if n < 3:
        raise ValueError('radar chart needs at least 3 axes')
    values = [max(0, min(100, v)) for v in values]

    def point(i, r):
        a = -math.pi / 2 + i * 2 * math.pi / n
        return cx + r * math.cos(a), cy + r * math.sin(a), math.cos(a)

    axes, texts, pts = [], [], []
    for i, (lab, val) in enumerate(zip(labels, values)):
        x, y, c = point(i, R)
        axes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')
        tx, ty, _ = point(i, R + 18)
        anchor = 'middle' if abs(c) < .5 else ('start' if c > 0 else 'end')
        texts.append(
            f'<text x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}">{escape(str(lab))}</text>'
        )
        px, py, _ = point(i, R * val / 100)
        pts.append(f'{px:.1f},{py:.1f}')

    grids = []
    for lvl in (20, 40, 60, 80, 100):
        gp = []
        for i in range(n):
            gx, gy, _ = point(i, R * lvl / 100)
            gp.append(f'{gx:.1f},{gy:.1f}')
        grids.append(f'<polygon points="{" ".join(gp)}"/>')

    doc = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;fill:{t['fg']};font-size:12px}}
.title{{font-size:16px;font-weight:700}}
.grid,.axis{{fill:none;stroke:{t['line']};stroke-width:1}}
.area{{fill:{t['accent']};fill-opacity:.16;stroke:{t['accent']};stroke-width:2}}</style>
<rect width="100%" height="100%" rx="18" fill="{t['bg']}"/>
<text x="{w // 2}" y="34" text-anchor="middle" class="title">{escape(title)}</text>
<g class="grid">{''.join(grids)}</g><g class="axis">{''.join(axes)}</g>
<polygon class="area" points="{' '.join(pts)}"/>{''.join(texts)}</svg>'''
    (ASSETS / filename).write_text(doc, encoding='utf-8')


def placeholder(filename, theme):
    path = ASSETS / filename
    if path.exists():  # keep the last good render
        return
    t = THEMES[theme]
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 300">'
        f'<rect width="100%" height="100%" rx="18" fill="{t["bg"]}"/>'
        f'<text x="260" y="135" text-anchor="middle" fill="{t["fg"]}" '
        f'font-family="monospace" font-size="16">GitHub language data</text>'
        f'<text x="260" y="165" text-anchor="middle" fill="{t["fg"]}" '
        f'font-family="monospace" font-size="12">Refresh via Actions</text></svg>',
        encoding='utf-8',
    )


# Self-assessed skills (dark + light)
for theme in THEMES:
    radar('Self-assessed skill areas', list(SELF), list(SELF.values()),
          f'radar-{theme}.svg', theme)

# GitHub language usage (dark + light)
try:
    langs = get_stats()['languages']
    top = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:8]
    if not top or top[0][1] <= 0:
        raise ValueError('no language data')
    labels = [k for k, _ in top]
    vals = [round(100 * v / top[0][1]) for _, v in top]
    for theme in THEMES:
        radar('GitHub language usage (relative)', labels, vals,
              f'radar-languages-{theme}.svg', theme)
except Exception as e:
    print(f'language radar skipped: {e}')
    for theme in THEMES:
        placeholder(f'radar-languages-{theme}.svg', theme)
