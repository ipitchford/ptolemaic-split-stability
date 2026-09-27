#!/usr/bin/env python3
"""Semantic negative controls, deliberately rehashing corrupted disposable inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODES = [('normal', [], None), ('flag-O', ['-O'], None),
         ('flag-OO', ['-OO'], None), ('env-1', [], '1'), ('env-2', [], '2')]

def manifest(root):
    paths = sorted(p for p in root.rglob('*') if p.is_file()
                   and p.name != 'SHA256SUMS' and '__pycache__' not in p.parts
                   and '.git' not in p.parts)
    (root / 'SHA256SUMS').write_text(''.join(
        hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(root).as_posix() + '\n'
        for p in paths))

def main(output):
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Output must be outside the bundle')
    output.mkdir(parents=True, exist_ok=True)
    records = []
    with tempfile.TemporaryDirectory(prefix='ptolemaic-mode-controls-') as temp:
        base = Path(temp)
        for mutation in ['valid', 'negative-small', 'identity-small', 'negative-symbolic', 'identity-symbolic']:
            root = base / mutation
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('__pycache__', '.git'))
            if mutation != 'valid':
                family = 'small' if mutation.endswith('small') else 'symbolic'
                path = root / 'certificates' / (family + '_duals.json')
                certs = json.loads(path.read_text())
                if mutation.startswith('negative'):
                    certs[0]['values'][0] = '-1'
                else:
                    certs[0]['values'][-1] = '(' + certs[0]['values'][-1] + ')+1'
                path.write_text(json.dumps(certs, indent=2) + '\n')
                manifest(root)
            scripts = ['verify_exact.py', 'verify_symbolic.py', 'verify_numerical.py'] if mutation == 'valid' else (
                ['verify_exact.py'] if mutation.endswith('small') else ['verify_exact.py', 'verify_symbolic.py'])
            for name, flags, optimization in MODES:
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
                env.pop('PYTHONOPTIMIZE', None)
                if optimization is not None:
                    env['PYTHONOPTIMIZE'] = optimization
                for entry in scripts + ['replay.py']:
                    dest = base / 'outputs' / mutation / name / entry
                    command = [sys.executable, *flags, '-B', str(root / (entry if entry == 'replay.py' else 'code/' + entry))]
                    if entry == 'replay.py':
                        command += ['--mode', 'exact']
                    command += ['--output', str(dest)]
                    run = subprocess.run(command, env=env, capture_output=True, text=True)
                    log = mutation + '-' + name + '-' + entry + '.log'
                    (output / log).write_text(run.stdout + run.stderr)
                    expected_pass = mutation == 'valid'
                    if (run.returncode == 0) != expected_pass:
                        raise RuntimeError('Unexpected verifier disposition: ' + log)
                    if not expected_pass and ('Hash mismatch' in run.stderr or 'PASS:' in run.stdout):
                        raise RuntimeError('Control did not test mathematical rejection: ' + log)
                    if not expected_pass:
                        for receipt in dest.rglob('*results.json'):
                            if json.loads(receipt.read_text()).get('status') == 'PASS':
                                raise RuntimeError('Invalid input produced a success result: ' + log)
                    records.append(dict(mutation=mutation, mode=name, entrypoint=entry,
                                        exitCode=run.returncode, expected='pass' if expected_pass else 'reject', log=log))
                    print(mutation, name, entry, 'PASS' if expected_pass else 'REJECTED', flush=True)
    (output / 'MODE_CONTROL_REPORT.json').write_text(json.dumps({
        'status': 'PASS', 'checks': records, 'corrupt_manifests_updated': True,
        'scope': 'Software acceptance controls, not formal proof of the analytic manuscript.'}, indent=2) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    main(parser.parse_args().output)
