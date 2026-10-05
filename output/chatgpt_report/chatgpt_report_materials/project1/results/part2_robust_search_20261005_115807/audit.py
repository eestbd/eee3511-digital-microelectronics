"""Independent raw-current, integration, sensitivity and preservation audit."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent


def read_csv(path,cstore,dt):
    f=pd.read_csv(path)
    assert len(f)==round(5e-10/dt)+1
    assert np.isfinite(f[['time_s','Vcell_V','VBL_V']].to_numpy()).all()
    assert abs(f.time_s.iloc[-1]-5e-10)<=1e-20
    assert np.allclose(np.diff(f.time_s),dt,rtol=1e-12,atol=1e-22)
    currents=f[['Id_A','Is_A','Ib_A']].iloc[1:].to_numpy()
    assert np.isfinite(currents).all()
    balance=abs(currents.sum(axis=1))
    assert np.all(balance<=np.maximum(1e-18,abs(currents).max(axis=1)*1e-6))
    cell=abs(np.diff(f.Vcell_V)+currents[:,1]*dt/cstore)
    bl=abs(np.diff(f.VBL_V)+currents[:,0]*dt/100e-15)
    assert cell.max()<=1e-12 and bl.max()<=1e-12
    residual=cstore*(f.Vcell_V.iloc[1:].to_numpy()-f.Vcell_V.iloc[0])
    residual+=100e-15*(f.VBL_V.iloc[1:].to_numpy()-1)
    residual-=np.cumsum(currents[:,2]*dt)
    assert abs(residual).max()<=1e-24
    return dict(passed=True,margin_V=float(abs(f.VBL_V.iloc[-1]-1)),
                max_charge_residual_C=float(abs(residual).max()),
                max_current_balance_A=float(balance.max()))


def hold_csv(path,cstore,delta):
    f=pd.read_csv(path)
    assert np.isfinite(f[['time_s','Vcell_V','dt_s']].to_numpy()).all()
    dt=np.diff(f.time_s);dv=np.diff(f.Vcell_V);current=f.Istorage_A.iloc[1:].to_numpy()
    assert np.isfinite(current).all() and (dt>0).all() and (dt<=.008+1e-12).all()
    assert abs(dv).max()<=delta+1e-12
    error=abs(dv+current*dt/cstore)
    assert error.max()<=1e-12
    observed=f.dropna(subset=['read_margin_V']) if 'read_margin_V' in f else None
    return dict(passed=True,rows=len(f),end_time_s=float(f.time_s.iloc[-1]),
                end_cell_V=float(f.Vcell_V.iloc[-1]),max_Euler_error_V=float(error.max()),
                observed_margin_monotonic=None if observed is None else bool(np.all(np.diff(observed.read_margin_V)<=1e-6)))


def audit(label):
    folder=RUN/'experiments'/label
    checks={};metrics={}
    for phase in ('verify','fine'):
        for bit in (0,1):
            name=f'{phase}{bit}';out=folder/name
            m=json.loads((out/'metrics.json').read_text())
            assert m['measurement_complete'] and 'error' not in m
            c=m['capacitance']['CSTORE_F'];delta=m['max_delta_V']
            assert abs(c-m['capacitance']['fine_CSTORE_F'])<=c*1e-6
            assert abs(c-m['capacitance']['reference_F'])<=c*.01
            assert m['extended_precision'] and m['ramp_step_V']==.1
            assert m['conditions']['retention_BL_V']==(2 if bit==0 else 0)
            initial=read_csv(out/'initial_read.csv',c,1e-11)
            fine=read_csv(out/'initial_read_5ps.csv',c,5e-12)
            assert abs(initial['margin_V']-m['initial_read']['margin_V'])<=1e-12
            assert abs(fine['margin_V']-m['initial_read']['fine_5ps_margin_V'])<=1e-12
            assert abs(initial['margin_V']-fine['margin_V'])<=.002
            reads=[]
            for checkpoint in m['degraded_reads']:
                checked=read_csv(out/f"degraded_read_{checkpoint['index']:03d}.csv",c,1e-11)
                assert abs(checked['margin_V']-checkpoint['margin_V'])<=1e-12
                reads.append(checked)
            h=hold_csv(out/'retention64.csv',c,delta)
            assert h['observed_margin_monotonic']
            ret=m['retention64'];retframe=pd.read_csv(out/'retention64.csv')
            if ret['failure_bracket_s'] is None:
                assert abs(h['end_time_s']-.064)<=1e-12
                assert (retframe.read_margin_V.dropna()>=.06).all()
            else:
                lo,hi=ret['failure_bracket_s'];assert lo<hi and (hi-lo)/hi<=.01
            extra=m.get('extended_retention')
            extcheck=None
            if extra:
                extcheck=hold_csv(out/'continuation.csv',c,delta)
                assert extcheck['observed_margin_monotonic']
                seed=next(r for r in m['degraded_reads'] if r['label']=='seed')
                assert abs(seed['margin_V']-m['margin_at_64ms_V'])<=5e-5
                if extra['failure_bracket_s']:
                    lo,hi=extra['failure_bracket_s'];assert .064<=lo<hi and (hi-lo)/hi<=.01
                    assert extra['bracket_READ_margins_V'][0]>=.06>extra['bracket_READ_margins_V'][1]
                    for trace in extra['refinement_trace']:
                        a=pd.DataFrame(trace['integration_steps'])
                        assert (a.dt_s>0).all() and (a.dt_s<=.008+1e-12).all()
                        assert abs(a.Vcell_V-a.initial_Vcell_V).max()<=delta+1e-12
                        assert abs(a.Vcell_V-a.initial_Vcell_V+a.Istorage_A*a.dt_s/c).max()<=1e-12
                else:
                    assert extra['end_margin_V']>=.06
            for path,digest in m['source_sha256'].items():
                assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
            assert hashlib.sha256((folder/'input.yaml').read_bytes()).hexdigest()==m['config_sha256']
            assert hashlib.sha256((folder/'screen/part2_diagnostic.devsim').read_bytes()).hexdigest()==m['structure_sha256']
            assert hashlib.sha256((RUN/'verify_candidate.py').read_bytes()).hexdigest()==m['measurement_script_sha256']
            assert hashlib.sha256((ROOT/'project1/results/retention_estimate_20261005_111911/measure.py').read_bytes()).hexdigest()==m['continuation_helper_sha256']
            physics=m['native_physics']
            assert abs(physics['mu_n']-202.9698962276924)<=1e-9
            assert abs(physics['mu_p']-107.38756563544702)<=1e-9
            assert abs(physics['n_i']-4757304128886.964)<=1e3
            assert physics['n_i']==physics['n1']==physics['p1']
            checks[name]=dict(passed=True,initial=initial,fine_read=fine,degraded_read_count=len(reads),
                              hold64=h,extension=extcheck)
            metrics[name]=m
    sensitivity={}
    for bit in (0,1):
        basic,fine=(metrics[f'{phase}{bit}'] for phase in ('verify','fine'))
        difference=abs(basic['margin_at_64ms_V']-fine['margin_at_64ms_V'])
        assert difference<=.002
        b,f=(m.get('extended_retention') for m in (basic,fine))
        relative=None
        if b and f and b.get('estimate_s') and f.get('estimate_s'):
            relative=abs(b['estimate_s']-f['estimate_s'])/max(b['estimate_s'],f['estimate_s'])
            assert relative<=.01
        sensitivity[str(bit)]=dict(margin64_difference_V=difference,estimate_relative_difference=relative)
    geometry=json.loads((RUN/'selected_geometry/validation.json').read_text())
    assert geometry['passed'] and geometry['structure_sha256']==metrics['verify1']['structure_sha256']
    data=yaml.safe_load((folder/'input.yaml').read_text())
    device,cap=data['device'],data['capacitor']
    bounds=geometry['bounds_um']
    tox_cm=(bounds['oxide']['ymax_um']-bounds['oxide']['ymin_um'])*1e-4
    tdiel_cm=(bounds['hk_l']['xmax_um']-bounds['hk_l']['xmin_um'])*1e-4
    assert tox_cm>=5e-7-1e-14 and 2.5/tox_cm/1e6<=5+1e-10
    assert 1/tdiel_cm/1e6<=4+1e-10
    assert .02<=device['junction_depth_um']<=.25 and .3<=device['silicon_thickness_um']<=2
    assert .2<=device['source_length_um']<=1 and .2<=device['drain_length_um']<=1
    assert 1e14<=device['body_doping_cm3']<=1e17 and 1e18<=device['sd_doping_cm3']<=1e21
    profile=data['doping_profile']
    assert all(1e14<=profile[key]<=1e17 for key in ('source_side_na_cm3','drain_side_na_cm3'))
    assert all(1e18<=profile[key]<=1e21 for key in ('source_nd_cm3','drain_nd_cm3'))
    assert .2<=cap['height_um']<=1.5 and 3<=cap['dielectric_nm']<=10
    assert cap['material'] in ('SiO2','Al2O3','HfO2','ZrO2')
    assert all(0<m['capacitance']['CSTORE_F']<=20e-15 for m in metrics.values())
    donor=json.loads((RUN/'donor_plateau_validation.json').read_text());assert donor['passed']
    result=dict(passed=True,all_minimum_specs_pass=all(m['minimum_specs_state_pass'] for m in metrics.values()),
                candidate=label,structure_sha256=metrics['verify1']['structure_sha256'],
                numerical_checks=checks,sensitivity=sensitivity,geometry_pass=True)
    assert result['all_minimum_specs_pass']
    (RUN/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


def preservation():
    snapshot=json.loads((RUN/'protected_snapshot.json').read_text())
    count=0
    for path,digest in snapshot.items():
        if path in ('PLAN.md','PROGRESS_LOG.md'):continue
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
        count+=1
    assert (ROOT/'PROGRESS_LOG.md').read_bytes().startswith((RUN/'prior_log.bin').read_bytes())
    assert subprocess.check_output(['git','diff','--cached','--binary'])==(RUN/'prior_staged.diff').read_bytes()
    subprocess.run(['git','diff','--check'],capture_output=True,check=True)
    return dict(passed=True,protected_files_unchanged=count,log_prefix_preserved=True,staged_state_preserved=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--candidate');args=parser.parse_args()
    if args.candidate: print(json.dumps(audit(args.candidate),indent=2))
    protected=preservation()
    (RUN/'preservation.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
    print(json.dumps(protected))
