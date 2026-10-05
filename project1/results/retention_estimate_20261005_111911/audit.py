"""Independent CSV, failure bracket, sensitivity and preservation checks."""
from pathlib import Path
import hashlib
import json
import subprocess

import numpy as np
import pandas as pd

root=Path.cwd()
run=root/'project1/results/retention_estimate_20261005_111911'
checks={}
metrics={}
for phase in ('primary','fine'):
    for bit in (1,0):
        name=f'{phase}_bit{bit}'
        folder=run/name
        metric=json.loads((folder/'metrics.json').read_text(encoding='utf-8'))
        assert metric['measurement_complete'] and 'error' not in metric
        assert metric['seed_replay_difference_V'] <= 5e-5
        metrics[name]=metric
        cstore=metric['CSTORE_F']
        frame=pd.read_csv(folder/'continuation.csv')
        dt=np.diff(frame.time_s)
        dv=np.diff(frame.Vcell_V)
        current=frame.Istorage_A.iloc[1:].to_numpy()
        assert np.isfinite(frame[['time_s','Vcell_V','dt_s']].to_numpy()).all()
        assert np.isfinite(current).all() and (dt>0).all() and (dt<=.008+1e-12).all()
        assert abs(dv).max() <= metric['max_delta_V']+1e-12
        assert abs(dv+current*dt/cstore).max() <= 1e-12
        observed=frame.dropna(subset=['read_margin_V'])
        assert np.all(np.diff(observed.read_margin_V)<=1e-6)
        read_checks=[]
        for checkpoint in metric['read_checkpoints']:
            read=pd.read_csv(folder/f"read_{checkpoint['index']:03d}.csv")
            assert len(read)==51 and abs(read.time_s.iloc[-1]-5e-10)<=1e-20
            assert np.allclose(np.diff(read.time_s),1e-11,rtol=1e-12,atol=1e-22)
            currents=read[['Id_A','Is_A','Ib_A']].iloc[1:].to_numpy()
            assert np.isfinite(currents).all()
            assert np.all(abs(currents.sum(axis=1)) <= np.maximum(1e-18,abs(currents).max(axis=1)*1e-6))
            assert abs(np.diff(read.Vcell_V)+currents[:,1]*1e-11/cstore).max()<=1e-12
            assert abs(np.diff(read.VBL_V)+currents[:,0]*1e-11/100e-15).max()<=1e-12
            residual=cstore*(read.Vcell_V.iloc[1:].to_numpy()-read.Vcell_V.iloc[0])
            residual+=100e-15*(read.VBL_V.iloc[1:].to_numpy()-1)
            residual-=np.cumsum(currents[:,2]*1e-11)
            assert abs(residual).max()<=1e-24
            assert abs(abs(read.VBL_V.iloc[-1]-1)-checkpoint['margin_V']) <= 1e-12
            read_checks.append(dict(index=checkpoint['index'], max_charge_residual_C=float(abs(residual).max())))
        ret=metric['retention']
        if bit==1:
            low, high=ret['failure_bracket_s']
            assert .064 <= low < high and (high-low)/high <= .001
            assert ret['bracket_READ_margins_V'][0] >= .060 > ret['bracket_READ_margins_V'][1]
            for trace in ret['refinement_trace']:
                steps=pd.DataFrame(trace['integration_steps'])
                assert (steps.dt_s>0).all() and (steps.dt_s<=.008+1e-12).all()
                assert abs(steps.Vcell_V-steps.initial_Vcell_V).max() <= metric['max_delta_V']+1e-12
                assert abs(steps.Vcell_V-steps.initial_Vcell_V+steps.Istorage_A*steps.dt_s/cstore).max() <= 1e-12
                assert abs(steps.time_s.iloc[-1]-trace['time_s']) <= 1e-12
            for t,margin in zip(ret['failure_bracket_s'],ret['bracket_READ_margins_V']):
                matches=[c for c in metric['read_checkpoints'] if abs(c['time_s']-t)<=1e-12 and abs(c['margin_V']-margin)<=1e-12]
                assert matches
        else:
            assert ret['failure_bracket_s'] is None and (observed.read_margin_V>=.06).all()
        for path, digest in metric['source_sha256'].items():
            assert hashlib.sha256((root/'project1'/path).read_bytes()).hexdigest()==digest
        assert hashlib.sha256((root/'project1/part2_2022142233.devsim').read_bytes()).hexdigest()==metric['structure_sha256']
        assert hashlib.sha256((run/'measure.py').read_bytes()).hexdigest()==metric['experiment_sha256']
        checks[name]=dict(passed=True, read_count=len(read_checks),
                         raw_rows=len(frame), seed_difference_V=metric['seed_replay_difference_V'],
                         max_Euler_residual_V=float(abs(dv+current*dt/cstore).max()),
                         read_checks=read_checks)
primary,fine=(metrics[f'{phase}_bit1']['retention'] for phase in ('primary','fine'))
difference=abs(primary['estimate_s']-fine['estimate_s'])
relative=difference/max(primary['estimate_s'],fine['estimate_s'])
assert relative <= .01
upper=max(primary['failure_bracket_s'][1],fine['failure_bracket_s'][1])
for phase in ('primary','fine'):
    ret=metrics[f'{phase}_bit0']['retention']
    assert ret['retention_lower_bound_s']>=upper-1e-12 and ret['end_margin_V']>=.06
snapshot=json.loads((root/'project1/tmp/retention_estimate_20261005_111911/start_snapshot.json').read_text(encoding='utf-8'))
protected=0
for path,digest in snapshot['file_sha256'].items():
    if path in ('PLAN.md','PROGRESS_LOG.md'):
        continue
    assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
    protected+=1
assert (root/'PROGRESS_LOG.md').read_bytes().startswith(bytes.fromhex(snapshot['log_prefix_hex']))
assert subprocess.check_output(['git','diff','--cached','--name-status','-z']).decode('utf-8')==snapshot['staged_state']
subprocess.run(['git','diff','--check'],check=True,capture_output=True)
result=dict(passed=True,cell_limiting_state='data1',cell_estimate_s=fine['estimate_s'],
            fine_cell_failure_bracket_s=fine['failure_bracket_s'],
            primary_cell_failure_bracket_s=primary['failure_bracket_s'],
            primary_fine_estimate_difference_s=difference,
            primary_fine_relative_difference=relative,
            combined_numerical_bracket_s=[min(primary['failure_bracket_s'][0],fine['failure_bracket_s'][0]),upper],
            data0_verified_lower_bound_s=min(metrics[f'{phase}_bit0']['retention']['retention_lower_bound_s'] for phase in ('primary','fine')),
            data0_required_confirmation_time_s=upper,
            data0_end_margins_V={phase:metrics[f'{phase}_bit0']['retention']['end_margin_V'] for phase in ('primary','fine')},
            raw_checks=checks,protected_files_unchanged=protected,
            old_log_prefix_preserved=True,staged_state_preserved=True)
(run/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='raw_checks'},indent=2))
