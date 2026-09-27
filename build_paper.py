#!/usr/bin/env python3
"""Build PDFs outside the immutable bundle using Pandoc and pdfLaTeX."""
import argparse,subprocess,shutil,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def build(source,title,subtitle,name,out):
    text=source.read_text()
    if source.name=='RESEARCH_NOTE.md':
        text='\n'.join(text.splitlines()[5:])
    else:
        text='\n'.join(text.splitlines()[1:])
    text=re.sub(r'https?://[^\s<>]+',lambda m:'<'+m.group(0).rstrip('.')+'>'+('.' if m.group(0).endswith('.') else ''),text)
    # A real line break in cases is two backslashes, not display delimiters.
    dest=out/name;dest.mkdir(parents=True,exist_ok=True)
    md=dest/'source.md';md.write_text(text)
    tex=dest/(name+'.tex')
    proc=subprocess.run(['pandoc',str(md),'-f','markdown+tex_math_dollars+raw_tex','-t','latex','--standalone','--template',str(ROOT/'paper/template.tex'),'-M','title='+title,'-M','subtitle='+subtitle,'-o',str(tex)],capture_output=True,text=True)
    (dest/'pandoc.log').write_text(proc.stdout+proc.stderr)
    if proc.returncode:raise RuntimeError(proc.stderr)
    for passno in range(2):
        p=subprocess.run(['pdflatex','-halt-on-error','-interaction=nonstopmode',tex.name],cwd=dest,capture_output=True,text=True)
        (dest/f'build_{passno+1}.log').write_text(p.stdout+p.stderr)
        if p.returncode:raise RuntimeError(f'LaTeX failed; see {dest}')
    log=(dest/(name+'.log')).read_text()
    problems=[line for line in log.splitlines() if any(t in line for t in ['Overfull','Missing character','undefined references','multiply defined'])]
    print(name, 'build complete;',len(problems),'flagged lines')
    for line in problems:print(line)
    return dest

def main(out):
    out=out.resolve()
    if out==ROOT or ROOT in out.parents:raise ValueError('Build output must be outside the bundle')
    out.mkdir(parents=True,exist_ok=True)
    build(ROOT/'RESEARCH_NOTE.md','Sharp local stability and critical-exponent sensitivity of Ptolemaic split metrics','All-cardinality first-order constants and the four-point transition','rigidity',out)
    build(ROOT/'review/RESPONSE_TO_REVIEW.md','Response and further development','Supplied v0.2 and research supplement v0.3','response',out)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
