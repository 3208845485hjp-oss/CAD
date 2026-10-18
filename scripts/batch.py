"""Batch edits on copies. Inputs are never passed to AutoCAD for writing."""
import argparse
import pathlib
import shutil
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--input', required=True, help='Folder of DWGs, non-recursive')
p.add_argument('--output', required=True, help='New empty output folder')
p.add_argument('--lisp', required=True, help='Reviewed AutoLISP file')
p.add_argument('--apply', action='store_true', help='Otherwise only list files')
a = p.parse_args()
src = pathlib.Path(a.input).resolve()
dst = pathlib.Path(a.output).resolve()
files = sorted(src.glob('*.dwg'))
if not files:
    raise SystemExit('No DWGs found')
if dst == src or src in dst.parents or dst in src.parents:
    raise SystemExit('Use separate, non-nested input and output folders')
if not pathlib.Path(a.lisp).is_file():
    raise SystemExit('LISP file not found')
if dst.exists() and any(dst.iterdir()):
    raise SystemExit('Output folder must be empty')
for f in files:
    print(f'{f} -> {dst / f.name}')
if not a.apply:
    raise SystemExit(0)
dst.mkdir(parents=True, exist_ok=True)
core = pathlib.Path(__file__).resolve().parents[1] / 'skills/cad-edit/scripts/core.py'
for f in files:
    if f.with_suffix('.dwl').exists() or f.with_suffix('.dwl2').exists():
        raise SystemExit(f'Drawing locked: {f}')
    copy = dst / f.name
    shutil.copy2(f, copy)
    subprocess.run([sys.executable, str(core), 'run', str(copy), '--timeout', '90', '--save', '--file', a.lisp], check=True)
    subprocess.run([sys.executable, str(core), 'info', str(copy), '--timeout', '90'], check=True)
