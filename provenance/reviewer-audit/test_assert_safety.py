"""Reviewer fault-injection test. Never modifies the submitted archive."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys
import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bundle', required=True, type=Path, help='Extracted v0.3 bundle root')
parser.add_argument('--output', required=True, type=Path, help='Fresh output directory; never the source bundle')
args = parser.parse_args()
source = args.bundle.resolve()
work = args.output.resolve()
if not (source/'certificates/small_duals.json').is_file():
    parser.error('--bundle is not an extracted v0.3 bundle root')
if work == source or source in work.parents:
    parser.error('--output must be outside the source bundle')
work.mkdir(parents=True, exist_ok=False)
copy = work/'disposable_mutated_bundle'
shutil.copytree(source, copy)
f = copy/'certificates/small_duals.json'
obj = json.loads(f.read_text())
old = obj[0]['values'][0]
obj[0]['values'][0] = '-1'
f.write_text(json.dumps(obj, indent=2)+'\n')
# Update the file-integrity manifest so this tests proof checking, not corruption detection.
manifest = copy/'SHA256SUMS'
lines = []
for line in manifest.read_text().splitlines():
    digest, relative = line.split('  ', 1)
    if relative == 'certificates/small_duals.json':
        digest = hashlib.sha256((copy/relative).read_bytes()).hexdigest()
    lines.append(digest+'  '+relative)
manifest.write_text('\n'.join(lines)+'\n')
results = {'mutation': {'record':0, 'field':'values[0]', 'from':old, 'to':'-1'},'manifest_updated':True,'original_untouched':True, 'runs':[]}
for mode in ['normal','optimised']:
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    if mode == 'optimised': env['PYTHONOPTIMIZE']='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    output = work/('fault_'+mode)
    p = subprocess.run([sys.executable, str(copy/'replay.py'), '--mode','exact','--output',str(output)],env=env,text=True,capture_output=True)
    rec={'mode':mode,'exit_code':p.returncode, 'stdout':p.stdout, 'stderr':p.stderr}
    if (output/'REPLAY_REPORT.json').exists(): rec['report']=json.loads((output/'REPLAY_REPORT.json').read_text())
    results['runs'].append(rec)
(work/'assert_safety_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'mutation':results['mutation'],'runs':[{'mode':r['mode'],'exit_code':r['exit_code'],'status':r.get('report',{}).get('status'), 'stdout':r['stdout']} for r in results['runs']]},indent=2))
