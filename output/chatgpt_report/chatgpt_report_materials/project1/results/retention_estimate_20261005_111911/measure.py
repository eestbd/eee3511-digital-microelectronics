"""Continuation of a verified 64 ms checkpoint; no device/model changes."""
from pathlib import Path
import argparse
import contextlib
import hashlib
import json
import math
import sys
import time
import traceback

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'project1'))
import devsim
from mosfet_tool.cell import Capacitor, CellSimulator, WIDTH_UM, read_transient, validate_currents
from mosfet_tool.config import Device

CONSOLE = sys.stdout

def announce(text):
    print(text, file=CONSOLE, flush=True)

def continue_hold(current, read_margin, start_t, start_v, end_t, cstore,
                  delta_v, bit, save, relative_bracket=.001):
    """Same signed leakage Euler/checkpoint READ as cell.retention, with a seed."""
    bl = 2.0 if bit == 0 else 0.0
    t, v = start_t, start_v
    m = read_margin(t, v, 'seed')
    if m < .060:
        raise RuntimeError('Verified continuation seed no longer passes READ')
    rows = [dict(time_s=t, Vcell_V=v, read_margin_V=m, dt_s=0., Istorage_A=None)]
    refinement = []
    last_t, last_v = t, v

    def advance(t0, v0, stop):
        records = []
        for _ in range(10000):
            if t0 >= stop:
                return v0, records
            currents = current(0., v0, bl)
            validate_currents(currents)
            amperes = currents['source'] * WIDTH_UM
            dt = min(.008, stop-t0, delta_v*cstore/abs(amperes) if amperes else .008)
            if t0 + dt == t0:
                raise RuntimeError('Continuation cannot advance time')
            old_v = v0
            v0 -= amperes*dt/cstore
            t0 += dt
            if not math.isfinite(v0) or not -.05 <= v0 <= 2.05:
                raise RuntimeError('Continuation voltage overshoot')
            records.append(dict(time_s=t0, Vcell_V=v0, initial_Vcell_V=old_v,
                                dt_s=dt, Istorage_A=amperes))
        raise RuntimeError('Continuation refinement step guard reached')

    for _ in range(10000):
        if t >= end_t:
            return rows, dict(failure_bracket_s=None, retention_lower_bound_s=t,
                              end_Vcell_V=v, end_margin_V=m, refinement_trace=refinement)
        currents = current(0., v, bl)
        validate_currents(currents)
        amperes = currents['source']*WIDTH_UM
        dt = min(.008, end_t-t, delta_v*cstore/abs(amperes) if amperes else .008)
        if t+dt == t:
            raise RuntimeError('Continuation cannot advance time')
        v -= amperes*dt/cstore
        t += dt
        if not math.isfinite(v) or not -.05 <= v <= 2.05:
            raise RuntimeError('Continuation voltage overshoot')
        check = abs(v-last_v) >= .03 or t-last_t >= .008 or t >= end_t
        m = read_margin(t, v, 'checkpoint') if check else None
        rows.append(dict(time_s=t, Vcell_V=v, read_margin_V=m, dt_s=dt, Istorage_A=amperes))
        save(rows, refinement)
        if check and m < .060:
            lo_t, lo_v, hi_t, hi_v = last_t, last_v, t, v
            lo_m = next(row['read_margin_V'] for row in reversed(rows[:-1]) if row['read_margin_V'] is not None)
            hi_m = m
            coarse = [lo_t, hi_t]
            for _ in range(40):
                if hi_t-lo_t <= max(1e-8, hi_t*relative_bracket):
                    break
                mid = (lo_t+hi_t)/2
                mid_v, advances = advance(lo_t, lo_v, mid)
                mid_m = read_margin(mid, mid_v, 'refinement')
                refinement.append(dict(time_s=mid, Vcell_V=mid_v, read_margin_V=mid_m,
                                       starts_at_time_s=lo_t, starts_at_Vcell_V=lo_v,
                                       integration_steps=advances))
                if mid_m >= .060:
                    lo_t, lo_v, lo_m = mid, mid_v, mid_m
                else:
                    hi_t, hi_v, hi_m = mid, mid_v, mid_m
                save(rows, refinement)
            return rows, dict(failure_bracket_s=[lo_t, hi_t], coarse_failure_bracket_s=coarse,
                              bracket_READ_margins_V=[lo_m, hi_m],
                              bracket_Vcell_V=[lo_v, hi_v], retention_lower_bound_s=lo_t,
                              estimate_s=(lo_t+hi_t)/2,
                              relative_bracket_width=(hi_t-lo_t)/hi_t, refinement_trace=refinement)
        if check:
            last_t, last_v = t, v
    raise RuntimeError('Continuation step guard reached')

def selftest():
    for bit, sign, seed_v, threshold, margin in (
        (0, -1, .064, .2, lambda v:.08-.1*v),
        (1, 1, 1.9, .164, lambda v:.06+.1*(v-1.8)),
    ):
        current = lambda *args:dict(source=sign*1e-13, drain=-sign*1e-13, body=0.)
        rows, result = continue_hold(current, lambda t,v,label:margin(v), .064, seed_v,
                                     .3, 10e-15, .003, bit, lambda *args:None)
        low, high = result['failure_bracket_s']
        assert low-1e-12 <= threshold <= high+1e-12
        assert result['bracket_READ_margins_V'][0] >= .06 > result['bracket_READ_margins_V'][1]
        assert result['relative_bracket_width'] <= .001
        a = pd.DataFrame(rows)
        assert np.max(abs(np.diff(a.Vcell_V)+a.Istorage_A.iloc[1:].to_numpy()*np.diff(a.time_s)/10e-15)) < 1e-12
    rows, result = continue_hold(lambda *args:dict(source=0.,drain=0.,body=0.),
                                 lambda *args:.08, .064, 0., .1, 10e-15, .003, 0,
                                 lambda *args:None)
    assert result['failure_bracket_s'] is None and result['retention_lower_bound_s'] == .1
    announce('PASS: analytic signed-current failures and no-failure continuation (3 cases)')

def run(args):
    started = time.monotonic()
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    config_path = ROOT/'project1/part2_final.yaml'
    structure = ROOT/'project1/part2_2022142233.devsim'
    original = ROOT/'project1/results/part2_optimization_20261004_202430/experiments/11_W_cap096_bodytap'/('combined_final' if args.phase=='primary' else 'combined_fine')
    metric = json.loads((original/'metrics.json').read_text(encoding='utf-8'))
    source_hash = {name:hashlib.sha256((ROOT/'project1'/name).read_bytes()).hexdigest() for name in metric['source_sha256']}
    assert source_hash == metric['source_sha256']
    assert hashlib.sha256(structure.read_bytes()).hexdigest() == metric['structure_sha256']
    assert (original/'config.yaml').read_bytes() == config_path.read_bytes()
    seed = pd.read_csv(original/f'retention_{args.bit}.csv').iloc[-1]
    delta_v = .003 if args.phase=='primary' else .0015
    data = yaml.safe_load(config_path.read_text(encoding='utf-8'))
    result = dict(phase=args.phase, bit=args.bit, measurement_complete=False,
                  source_sha256=source_hash, structure_sha256=metric['structure_sha256'],
                  experiment_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  original_metrics=original.relative_to(ROOT).as_posix()+'/metrics.json',
                  seed_time_s=float(seed.time_s), seed_Vcell_V=float(seed.Vcell_V),
                  original_seed_margin_V=float(seed.read_margin_V),
                  max_delta_V=delta_v, max_step_s=.008, max_time_s=args.stop_time,
                  READ_dt_s=1e-11, READ_decision_s=5e-10, margin_threshold_V=.060,
                  relative_bracket_goal=.001, extended_precision=True, ramp_step_V=.1)
    def save_result():
        result['elapsed_s']=time.monotonic()-started
        (output/'metrics.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    read_index = 0
    try:
        with (output/'native.log').open('w',encoding='utf-8') as native, contextlib.redirect_stdout(native):
            for name in ('extended_solver','extended_model','extended_equation'):
                devsim.set_parameter(name=name,value=True)
            sim = CellSimulator(Device(**data['device']), Capacitor(**data['capacitor']))
            sim.load_structure(structure)
            sim.solve_equilibrium()
            cstore, plate_points = sim.extract_capacitance(.01)
            assert math.isclose(cstore,metric['capacitance']['CSTORE_F'],rel_tol=1e-9)
            result['CSTORE_F']=cstore
            result['plate_points']=plate_points
            sim.enable_transport()
            def read(t,v,label):
                nonlocal read_index
                frame, measured=read_transient(sim.current_at,v,cstore)
                assert measured['max_charge_residual_C'] <= 1e-24
                frame.to_csv(output/f'read_{read_index:03d}.csv',index=False)
                record=dict(index=read_index,time_s=t,Vcell_V=v,label=label,**measured)
                result.setdefault('read_checkpoints',[]).append(record)
                read_index+=1
                if label=='seed':
                    difference=abs(measured['margin_V']-float(seed.read_margin_V))
                    result['seed_replay_difference_V']=difference
                    assert difference <= 5e-5, ('Seed READ does not reproduce',difference)
                save_result()
                announce(f"{args.phase} bit{args.bit} {label}: t={t*1000:.6f} ms Vcell={v:.9f} margin={measured['margin_V']*1000:.6f} mV")
                return measured['margin_V']
            def save(rows,refinement):
                pd.DataFrame(rows).to_csv(output/'continuation.csv',index=False)
                (output/'refinement.json').write_text(json.dumps(refinement,indent=2),encoding='utf-8')
            rows, measured=continue_hold(sim.current_at,read,float(seed.time_s),float(seed.Vcell_V),
                                         args.stop_time,cstore,delta_v,args.bit,save)
            save(rows,measured['refinement_trace'])
            result['retention']=measured
            result['measurement_complete']=True
    except Exception as error:
        result['error']=dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc())
        announce(result['error']['traceback'])
    save_result()
    announce(json.dumps({k:result.get(k) for k in ('phase','bit','measurement_complete','retention','elapsed_s','error')},default=str))
    return 1 if 'error' in result else 0

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--selftest',action='store_true')
    parser.add_argument('--phase',choices=('primary','fine'),default='primary')
    parser.add_argument('--bit',type=int,choices=(0,1),default=1)
    parser.add_argument('--stop-time',type=float,default=1.)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.selftest:
        selftest()
    else:
        assert args.output is not None and .064 < args.stop_time <= 1.
        raise SystemExit(run(args))
