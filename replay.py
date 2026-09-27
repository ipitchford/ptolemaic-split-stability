#!/usr/bin/env python3
"""Integrity-checked replay. Proof roles are recorded explicitly, not inferred from PASS."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def integrity():
    manifest=ROOT/'SHA256SUMS'
    if not manifest.exists():raise RuntimeError('SHA256SUMS is missing')
    count=0
    for line in manifest.read_text().splitlines():
        if not line.strip():continue
        want,rel=line.split('  ',1)
        p=(ROOT/rel).resolve()
        if ROOT not in p.parents or not p.is_file():raise RuntimeError('Unsafe or absent manifest member: '+rel)
        got=sha(p)
        if got!=want:raise RuntimeError('Hash mismatch: '+rel)
        count+=1
    return count

def main(mode,out):
    out=out.resolve()
    if out==ROOT or ROOT in out.parents:raise ValueError('Output must be outside the immutable bundle')
    out.mkdir(parents=True,exist_ok=True)
    report={'version':'0.3.1-candidate','mode':mode,'status':'RUNNING','formal_proof_assistant':False,
       'scope':'Exact algebra and certificates plus optional numerical corroboration; not formal verification of the analytic proof.',
       'manifest_files_verified':integrity(),'jobs':[]}
    jobs=[('exact','verify_exact.py',['exact_results.json']),
          ('symbolic','verify_symbolic.py',['symbolic_results.json'])]
    if mode=='full':jobs.append(('numerical','verify_numerical.py',['numerical_results.json','numerical_trials.json']))
    for name,script,outputs in jobs:
        dest=out/name;dest.mkdir(exist_ok=True)
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        start=time.monotonic()
        optimization = ['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else []
        p=subprocess.run([sys.executable,*optimization,str(ROOT/'code'/script),'--output',str(dest)],capture_output=True,text=True,env=env)
        (out/(name+'.log')).write_text(p.stdout+p.stderr)
        rec={'job':name,'exit_code':p.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'reports':{}}
        if p.returncode:
            report['jobs'].append(rec);report['status']='FAIL';(out/'REPLAY_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
            raise RuntimeError(f'{name} failed; read {out/name}.log')
        for filename in outputs:
            generated=dest/filename;shipped=ROOT/'results'/filename
            obj=json.loads(generated.read_text())
            if isinstance(obj,dict) and obj.get('status')!='PASS':raise RuntimeError(f'{filename} self-reports failure')
            same=sha(generated)==sha(shipped)
            rec['reports'][filename]={'matches_shipped_bytes':same,'exact_byte_match_required':name!='numerical','sha256':sha(generated)}
            if name!='numerical' and not same:raise RuntimeError(f'Exact report changed: {filename}')
        report['jobs'].append(rec)
    report['manifest_files_verified_after_replay']=integrity();report['status']='PASS'
    (out/'REPLAY_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS:',len(report['jobs']),'jobs;',report['manifest_files_verified'],'manifested files')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['exact','full'],default='exact');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.mode,a.output)
