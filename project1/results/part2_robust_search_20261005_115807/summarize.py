"""Derived experiment matrix; missing tests stay explicitly unmeasured."""
from pathlib import Path
import csv
import json
import yaml

RUN=Path(__file__).resolve().parent
rows=[]
for item in json.loads((RUN/'candidate_registry.json').read_text()):
    label=item['label'];folder=RUN/'experiments'/label
    config=yaml.safe_load((folder/'input.yaml').read_text())
    d,c=config['device'],config['capacitor']
    row=dict(candidate=label,screen_status='not_run',READ0_mV=None,READ1_mV=None,
             CSTORE_fF=None,Egate_MV_cm=None,Ecap_MV_cm=None,Istorage1_pA=None,
             endpoint1_64ms_mV=None,endpoint1_pass=None,full_verification_status='not_run',
             gate=d['gate_material'],tox_nm=d['oxide_thickness_nm'],xj_um=d['junction_depth_um'],
             NA_cm3=d['body_doping_cm3'],cap_height_um=c['height_um'],cap_tdiel_nm=c['dielectric_nm'],
             doping_profile=json.dumps(config.get('doping_profile')),body_tap=json.dumps(config.get('body_tap')),
             error=None)
    path=folder/'screen/metrics.json'
    if path.exists():
        m=json.loads(path.read_text())
        row['screen_status']='error' if m.get('error') else m.get('early_rejection') or ('complete' if m['measurement_complete'] else 'running')
        row['error']=m.get('error',{}).get('message')
        row['CSTORE_fF']=m.get('capacitance',{}).get('CSTORE_F',0)*1e15
        row['Egate_MV_cm']=m.get('fields',{}).get('gate_MV_cm')
        row['Ecap_MV_cm']=m.get('fields',{}).get('capacitor_MV_cm')
        for bit in ('0','1'):
            if bit in m.get('read',{}):row[f'READ{bit}_mV']=m['read'][bit]['margin_V']*1000
        if m.get('off_currents'):row['Istorage1_pA']=m['off_currents'][0]['Istorage_A']*1e12
    path=folder/'endpoint1/metrics.json'
    if path.exists():
        m=json.loads(path.read_text());e=m.get('endpoint1',{})
        if e:row['endpoint1_64ms_mV']=e['read_margin_V']*1000;row['endpoint1_pass']=e['endpoint_pass']
        if m.get('error'):row['error']=m['error']['message']
    phases=[]
    for phase in ('verify0','verify1','fine0','fine1'):
        path=folder/phase/'metrics.json'
        if path.exists():
            m=json.loads(path.read_text());phases.append(phase+':'+('error' if m.get('error') else 'complete' if m['measurement_complete'] else 'running'))
    if phases:row['full_verification_status']='; '.join(phases)
    rows.append(row)
(RUN/'results_matrix.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
with (RUN/'results_matrix.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
for row in rows:
    if row['screen_status']!='not_run':
        print(json.dumps({key:row[key] for key in ('candidate','screen_status','READ1_mV','Istorage1_pA','endpoint1_64ms_mV','full_verification_status')},ensure_ascii=False))
