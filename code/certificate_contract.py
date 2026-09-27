"""Require complete certificate coverage; an empty or truncated file is not a proof."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMALL_CONSTANTS = {(2,3): '6/5', (2,4): '3/2', (3,3): '9/5',
                   (3,4): '3', (3,5): '60/11', (4,4): '5'}

def load_certificates(family):
    records = json.loads((ROOT / 'certificates' / (family + '_duals.json')).read_text())
    if family == 'small':
        keys = [(r['a'],r['r'],r['typ'],r['sign']) for r in records]
        expected = {(a,b,t,s) for a,b in SMALL_CONSTANTS for t in ['A','X','B'] for s in [-1,1]}
    else:
        keys = [(r['offset'],r['kind'],r['sign']) for r in records]
        expected = {(d,t,s) for d in range(3) for t in ['A','X','B'] for s in [-1,1]}
        if any(r['k_min'] != (5 if r['offset'] == 0 else 4) for r in records):
            raise ValueError('Changed universal certificate domain')
    if len(keys) != len(expected) or set(keys) != expected:
        raise ValueError('Incomplete, duplicate or unexpected certificate family')
    for record in records:
        orbits = [tuple(o) for o in record['orbits']]
        if len(set(orbits)) != len(orbits) or len(record['values']) != len(orbits)+1:
            raise ValueError('Malformed orbit/weight vector')
    return records
