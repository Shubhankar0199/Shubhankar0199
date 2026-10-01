#!/usr/bin/env python3
import argparse, math
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

def esc(v):
    return str(v).replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')

def main():
    p=argparse.ArgumentParser(description='Convert a portrait into an SVG dot-matrix portrait.')
    p.add_argument('input'); p.add_argument('--output',default='assets/portrait.svg')
    p.add_argument('--cols',type=int,default=100); p.add_argument('--detail',type=float,default=.5)
    p.add_argument('--dot-size',type=float,default=0.8); p.add_argument('--contrast',type=float,default=1.08)
    p.add_argument('--brightness',type=float,default=1.0); p.add_argument('--threshold',type=int,default=0)
    p.add_argument('--color',action='store_true'); p.add_argument('--monochrome',action='store_true')
    p.add_argument('--invert',action='store_true'); p.add_argument('--reveal',action='store_true')
    a=p.parse_args()
    im=Image.open(a.input).convert('RGB')
    ratio=im.height/im.width
    rows=max(1,int(a.cols*ratio*.72))
    im=ImageOps.fit(im,(a.cols,rows),method=Image.Resampling.LANCZOS)
    im=ImageEnhance.Contrast(im).enhance(a.contrast)
    im=ImageEnhance.Brightness(im).enhance(a.brightness)
    out=[]
    bg='#0d1117'; green='#39d353'
    for y in range(rows):
        for x in range(a.cols):
            r,g,b=im.getpixel((x,y)); lum=(0.2126*r+0.7152*g+0.0722*b)/255
            if a.invert: lum=1-lum
            if a.threshold and int(lum*255)<a.threshold: lum=.05
            density=(1-lum)
            # keep enough structure while avoiding a noisy silhouette
            radius=.18 + (density**.82)*(a.dot_size*(0.45+0.55*a.detail))
            if density < .18 or radius < .28: continue
            if a.color and not a.monochrome:
                c=f'#{r:02x}{g:02x}{b:02x}'
                # tint toward GitHub green while retaining facial structure
                mix=.30
                rr=int(r*(1-mix)+57*mix); gg=int(g*(1-mix)+211*mix); bb=int(b*(1-mix)+83*mix)
                c=f'#{rr:02x}{gg:02x}{bb:02x}'
                opacity=.28+.72*density
            else:
                c=green; opacity=.18+.82*density
            out.append((x+0.5,y+0.5,radius,c,opacity))
    width=a.cols; height=rows
    style='''<style> .dot{animation:fadeIn .9s ease both;} @keyframes fadeIn{from{opacity:0;transform:scale(.15)}to{opacity:var(--o);transform:scale(1)}} </style>'''
    circles=[]
    total=max(1,len(out))
    for i,(x,y,r,c,o) in enumerate(out):
        delay=(i/total)*1.7 if a.reveal else 0
        anim=f' class="dot" style="--o:{o:.3f};animation-delay:{delay:.3f}s"' if a.reveal else ''
        circles.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{c}" opacity="{o:.3f}"{anim}/>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Dot matrix portrait of Shubhankar Pratap Singh">
<rect width="100%" height="100%" fill="{bg}"/>{style if a.reveal else ''}<g shape-rendering="geometricPrecision">{''.join(circles)}</g></svg>'''
    path=Path(a.output); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(svg,encoding='utf-8')
    print(f'Wrote {path} with {len(out)} dots')
if __name__=='__main__': main()
