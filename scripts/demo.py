"""Generate, save and reopen a native DWG using AutoCAD; never edits user drawings."""
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/cad-edit/scripts'))
import core


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    a = p.parse_args()
    out = pathlib.Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    dwg = out / 'demo.dwg'
    if dwg.exists():
        raise SystemExit('Output exists; choose a new directory.')
    import ezdxf
    d = ezdxf.new('R2018')
    d.units = 4
    d.layers.new('CAD-DEMO', dxfattribs={'color': 3})
    m = d.modelspace()
    m.add_lwpolyline([(0, 0), (6000, 0), (6000, 4000), (0, 4000)], close=True,
                     dxfattribs={'layer': 'CAD-DEMO'})
    m.add_circle((3000, 2000), 500, dxfattribs={'layer': 'CAD-DEMO'})
    seed = out / 'seed.dxf'
    d.saveas(seed)
    target = dwg.as_posix()
    lines = ['(setvar "OSMODE" 0)', '(command "_.UCS" "_W")',
             '(command "_.BOX" "8000,0,0" "10000,1000,0" "1500")',
             '(command "_.ZOOM" "_E")',
             f'(command "_.SAVEAS" "2018" "{target}")']
    result, elapsed, scr = core.run_core(str(seed), core.build_scr(lines), timeout=90, tag='demo')
    (out / 'create.log').write_text(result, encoding='utf-8')
    if core.show(result, True) or not dwg.exists():
        raise SystemExit('DWG creation failed; see create.log')
    check = ['(princ (strcat "\\nCHECK|poly=" (itoa (sslength (ssget "_X" (list (cons 0 "LWPOLYLINE"))))) "|circle=" (itoa (sslength (ssget "_X" (list (cons 0 "CIRCLE"))))) "|solid=" (itoa (sslength (ssget "_X" (list (cons 0 "3DSOLID"))))) "|units=" (itoa (getvar "INSUNITS"))))']
    actual, _, _ = core.run_core(str(dwg), core.build_scr(check), readonly=True, timeout=90, tag='verify')
    (out / 'reopen.log').write_text(actual, encoding='utf-8')
    ok = 'CHECK|poly=1|circle=1|solid=1|units=4' in actual and dwg.read_bytes()[:6] == b'AC1032'
    report = {'passed': ok, 'dwg': str(dwg), 'expected': {'closed_rectangle_mm': [6000,4000], 'circle_radius_mm':500, 'box_mm':[2000,1000,1500]}, 'engine': core.find_exe(), 'seconds':elapsed,
              'scope':'Synthetic example, not a reconstruction of the attached floor plan.'}
    (out / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
