"""Export a verified candidate and summarize measured evidence without overwrites."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
FOLDER=RUN/'experiments/19_balanced_ND20'


def measurements():
    records={}
    for phase in ('verify','fine'):
        for bit in (0,1):
            name=f'{phase}{bit}'
            m=json.loads((FOLDER/name/'metrics.json').read_text())
            assert m['measurement_complete'] and 'error' not in m
            assert m['minimum_specs_state_pass'] and m['extended_retention']
            records[name]=m
    hashes={m['structure_sha256'] for m in records.values()}
    assert len(hashes)==1
    upper=max(records[p+'1']['extended_retention']['failure_bracket_s'][1] for p in ('verify','fine'))
    for phase in ('verify','fine'):
        r=records[phase+'0']['extended_retention']
        assert r['failure_bracket_s'] is None and r['retention_lower_bound_s']>=upper
    return records


def export():
    records=measurements()
    directory=RUN/'selected'
    directory.mkdir(exist_ok=False)
    source=FOLDER/'screen/part2_diagnostic.devsim'
    destination=directory/'part2_2022142233.devsim'
    destination.write_bytes(source.read_bytes())
    config=ROOT/'project1/part2_robust.yaml'
    assert not config.exists(), 'Preserve existing configuration'
    config.write_bytes((FOLDER/'input.yaml').read_bytes())
    (directory/'config.yaml').write_bytes(config.read_bytes())
    digest=hashlib.sha256(destination.read_bytes()).hexdigest()
    assert digest==records['verify1']['structure_sha256']
    evidence=dict(candidate='19_balanced_ND20',status='pending_final_raw_audit',
                  structure=destination.relative_to(ROOT).as_posix(),
                  config=config.relative_to(ROOT).as_posix(),structure_sha256=digest,
                  baseline_root_structure_preserved=True)
    (RUN/'export.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print(json.dumps(evidence))


def finalize():
    validation=json.loads((RUN/'validation.json').read_text())
    assert validation['passed'] and validation['all_minimum_specs_pass']
    records=measurements()
    baseline=json.loads((ROOT/'project1/results/retention_estimate_20261005_111911/validation.json').read_text())
    b,f=(records[p+'1']['extended_retention'] for p in ('verify','fine'))
    now=datetime.now(timezone.utc)
    session=json.loads((RUN/'session.json').read_text())
    assert now<=datetime.fromisoformat(session['deadline_utc'])
    kst=now.astimezone(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S KST')
    elapsed=(now-datetime.fromisoformat(session['start_utc'])).total_seconds()/60
    summary=dict(candidate='19_balanced_ND20',completed_KST=kst,elapsed_min=elapsed,
                 all_minimum_specs_pass=True,cell_limiting_state='data1',
                 cell_estimate_s=f['estimate_s'],cell_failure_bracket_s=f['failure_bracket_s'],
                 primary_cell_estimate_s=b['estimate_s'],primary_failure_bracket_s=b['failure_bracket_s'],
                 baseline_cell_estimate_s=baseline['cell_estimate_s'],
                 cell_estimate_improvement_fraction=f['estimate_s']/baseline['cell_estimate_s']-1,
                 data0_retention_verified_lower_bound_s=.128,
                 data0_128ms_margins_V={p:records[p+'0']['extended_retention']['end_margin_V'] for p in ('verify','fine')},
                 initial_read_margins_V={p:{str(bit):records[p+str(bit)]['initial_read']['margin_V'] for bit in (0,1)} for p in ('verify','fine')},
                 margin64_V={p:{str(bit):records[p+str(bit)]['margin_at_64ms_V'] for bit in (0,1)} for p in ('verify','fine')},
                 CSTORE_F=records['verify1']['capacitance']['CSTORE_F'],
                 fields=records['verify1']['fields'],structure_sha256=records['verify1']['structure_sha256'],
                 screened_candidates=12,endpoint_compared_candidates=2,
                 extra_parameter_search_stopped=True,
                 limitations=['local official model; grader and independent mesh unverified',
                              'data0 maximum retention not measured',
                              'finite failure bracket, not a statistical confidence interval',
                              'aspirational 75mV/64mV/96ms goals not all achieved',
                              'final submission report/screenshots remain separate'])
    difference=abs(b['estimate_s']-f['estimate_s'])
    replacements={
        'COMPLETED_KST':kst,'ELAPSED_MIN':f'{elapsed:.1f}',
        'FINE_ESTIMATE_MS':f"{f['estimate_s']*1000:.6f}",
        'BASIC_ESTIMATE_MS':f"{b['estimate_s']*1000:.6f}",
        'IMPROVEMENT_PERCENT':f"{summary['cell_estimate_improvement_fraction']*100:.2f}",
        'BASIC_BRACKET_MS':' ~ '.join(f'{v*1000:.6f}' for v in b['failure_bracket_s']),
        'FINE_BRACKET_MS':' ~ '.join(f'{v*1000:.6f}' for v in f['failure_bracket_s']),
        'FINE_BRACKET_MARGINS':' / '.join(f'{v*1000:.6f}' for v in f['bracket_READ_margins_V']),
        'ESTIMATE_DIFFERENCE_MS':f'{difference*1000:.6f}',
        'ESTIMATE_RELATIVE_PERCENT':f"{difference/max(b['estimate_s'],f['estimate_s'])*100:.4f}",
        'FINE_END0':f"{records['fine0']['extended_retention']['end_margin_V']*1000:.6f}",
        'CSTORE_FF':f"{summary['CSTORE_F']*1e15:.6f}",
        'STRUCTURE_SHA256':summary['structure_sha256'],
    }
    for bit in (0,1):
        replacements['INITIAL'+str(bit)]=f"{records['verify'+str(bit)]['initial_read']['margin_V']*1000:.6f}"
        replacements['FINE_INITIAL'+str(bit)]=f"{records['fine'+str(bit)]['initial_read']['margin_V']*1000:.6f}"
        replacements['MARGIN'+str(bit)]=f"{records['verify'+str(bit)]['margin_at_64ms_V']*1000:.6f}"
        replacements['FINE_MARGIN'+str(bit)]=f"{records['fine'+str(bit)]['margin_at_64ms_V']*1000:.6f}"
    document=(RUN/'report_template.md').read_text(encoding='utf-8')
    for key,value in replacements.items():document=document.replace('{{'+key+'}}',value)
    assert '{{' not in document and '\ufffd' not in document and '??' not in document
    report=ROOT/'project1/PART2_ROBUST_SEARCH.md'
    assert not report.exists()
    report.write_text(document,encoding='utf-8')
    (RUN/'result_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    exported=json.loads((RUN/'export.json').read_text());exported['status']='verified_recommendation'
    (RUN/'export.json').write_text(json.dumps(exported,indent=2),encoding='utf-8')
    selection=json.loads((RUN/'selection.json').read_text());selection.update(status='verified_recommendation',minimum_specs_not_yet_fully_verified=False,completed_KST=kst)
    (RUN/'selection.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('export','finalize'));args=parser.parse_args()
    export() if args.stage=='export' else finalize()
