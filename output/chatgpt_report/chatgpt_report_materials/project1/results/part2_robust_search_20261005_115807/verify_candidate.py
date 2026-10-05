"""Fresh per-state characterization using unchanged official cell algorithms."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'project1'))
import devsim
import pandas as pd
import yaml
from mosfet_tool.cell import Capacitor, CellSimulator, read_transient, retention
from mosfet_tool.config import Device

HELPER = ROOT / 'project1/results/retention_estimate_20261005_111911/measure.py'
spec = importlib.util.spec_from_file_location('verified_continuation', HELPER)
continuation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(continuation)


def run(args):
    start = time.monotonic()
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    data = yaml.safe_load(args.config.read_text(encoding='utf-8'))
    (output / 'config.yaml').write_bytes(args.config.read_bytes())
    sources = [ROOT/'project1/part2.py', ROOT/'project1/part2_design.py',
               ROOT/'project1/check_structure_file.py',
               *sorted((ROOT/'project1/mosfet_tool').glob('*.py'))]
    result = dict(bit=args.bit, max_delta_V=args.delta, extended_precision=True,
                  ramp_step_V=.1, measurement_complete=False,
                  structure_file=str(args.structure),
                  structure_sha256=hashlib.sha256(args.structure.read_bytes()).hexdigest(),
                  config_sha256=hashlib.sha256(args.config.read_bytes()).hexdigest(),
                  source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sources},
                  measurement_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  continuation_helper_sha256=hashlib.sha256(HELPER.read_bytes()).hexdigest(),
                  conditions=dict(T_K=398, VB_V=-.5, WL_high_V=2.5, CBL_F=100e-15,
                                  width_um=.1, READ_dt_s=1e-11, READ_time_s=5e-10,
                                  retention_BL_V=2. if args.bit==0 else 0.,
                                  retention_max_dt_s=.008, margin_threshold_V=.060),
                  degraded_reads=[])

    def save():
        result['elapsed_s'] = time.monotonic()-start
        (output/'metrics.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')

    def checkpoint(name):
        save()
        (output/(name+'_checkpoint.json')).write_bytes((output/'metrics.json').read_bytes())

    try:
        for name in ('extended_solver','extended_model','extended_equation'):
            devsim.set_parameter(name=name, value=True)
        sim = CellSimulator(Device(**data['device']), Capacitor(**data['capacitor']))
        sim.load_structure(args.structure)
        checker = subprocess.run([sys.executable,'-B',str(ROOT/'project1/check_structure_file.py'),str(args.structure)],
                                 capture_output=True, text=True, encoding='utf-8')
        (output/'checker.log').write_text(checker.stdout+checker.stderr, encoding='utf-8')
        assert checker.returncode==0
        result['structure_check_passed']=True
        sim.solve_equilibrium()
        cstore, points=sim.extract_capacitance(.01)
        fine_c, fine_points=sim.extract_capacitance(.005)
        reference=sim.capacitor.parallel_plate_f
        assert 0<cstore<=20e-15
        assert abs(cstore-fine_c)<=cstore*1e-6 and abs(cstore-reference)<=reference*.01
        gate_field=2.5/(data['device']['oxide_thickness_nm']*1e-7)/1e6
        cap_field=1/(data['capacitor']['dielectric_nm']*1e-7)/1e6
        assert gate_field<=5 and cap_field<=4
        result['capacitance']=dict(CSTORE_F=cstore,fine_CSTORE_F=fine_c,reference_F=reference,
                                   plate_points=points,fine_plate_points=fine_points,passed=True)
        result['fields']=dict(gate_MV_cm=gate_field,capacitor_MV_cm=cap_field)
        checkpoint('capacitance')
        sim.enable_transport()
        result['native_physics']={name:devsim.get_parameter(device=sim.name,region='bulk',name=name)
                                  for name in ('mu_n','mu_p','n_i','n1','p1')}
        initial=0. if args.bit==0 else 2.
        frame, measured=read_transient(sim.current_at,initial,cstore)
        frame.to_csv(output/'initial_read.csv',index=False)
        fine_frame, fine_measured=read_transient(sim.current_at,initial,cstore,5e-12)
        fine_frame.to_csv(output/'initial_read_5ps.csv',index=False)
        measured['fine_5ps_margin_V']=fine_measured['margin_V']
        measured['step_sensitivity_V']=abs(measured['margin_V']-fine_measured['margin_V'])
        measured['step_validation_pass']=measured['step_sensitivity_V']<=.002
        assert measured['max_charge_residual_C']<=1e-24 and fine_measured['max_charge_residual_C']<=1e-24
        result['initial_read']=measured
        checkpoint('initial_read')

        def read(t,v,label):
            index=len(result['degraded_reads'])
            f,m=read_transient(sim.current_at,v,cstore)
            assert m['max_charge_residual_C']<=1e-24
            f.to_csv(output/f'degraded_read_{index:03d}.csv',index=False)
            result['degraded_reads'].append(dict(index=index,time_s=t,Vcell_V=v,label=label,**m))
            save()
            print(f"bit{args.bit} delta={args.delta} {label} t={t} Vcell={v:.9f} margin_mV={m['margin_V']*1000:.6f}",flush=True)
            return m['margin_V']

        frame, measured=retention(sim.current_at,lambda v:read(None,v,'retention64'),
                                  initial,cstore,max_delta_v=args.delta)
        frame.to_csv(output/'retention64.csv',index=False)
        result['retention64']=measured
        result['margin_at_64ms_V']=float(frame.read_margin_V.iloc[-1]) if measured['failure_bracket_s'] is None else None
        result['minimum_specs_state_pass']=bool(measured['passed'] and result['initial_read']['passed']
                                                and result['initial_read']['step_validation_pass'])
        checkpoint('retention64')
        if measured['failure_bracket_s'] is None and args.stop_time>.064:
            seed=frame.iloc[-1]
            def save_cont(rows,refinement):
                pd.DataFrame(rows).to_csv(output/'continuation.csv',index=False)
                (output/'refinement.json').write_text(json.dumps(refinement,indent=2),encoding='utf-8')
            rows,ret=continuation.continue_hold(sim.current_at,read,float(seed.time_s),float(seed.Vcell_V),
                                               args.stop_time,cstore,args.delta,args.bit,save_cont,
                                               relative_bracket=.01)
            save_cont(rows,ret['refinement_trace'])
            result['extended_retention']=ret
        result['measurement_complete']=True
    except Exception as error:
        result['error']=dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc())
        print(result['error']['traceback'],flush=True)
    save()
    print(json.dumps({k:result.get(k) for k in ('bit','measurement_complete','minimum_specs_state_pass','margin_at_64ms_V','extended_retention','error','elapsed_s')},indent=2),flush=True)
    return 1 if 'error' in result else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--structure',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--bit',type=int,choices=(0,1),required=True)
    parser.add_argument('--delta',type=float,default=.003)
    parser.add_argument('--stop-time',type=float,default=.128)
    args=parser.parse_args()
    assert args.delta in (.003,.0015) and .064<=args.stop_time<=1.
    raise SystemExit(run(args))
