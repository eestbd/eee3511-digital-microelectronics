import datetime,json,os,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[3]
run=Path(__file__).resolve().parent
label,stage=sys.argv[1:3]
folder=run/'experiments'/label
out=folder/stage
log=folder/(stage+'.log')
args=[str(root/'.conda/python.exe'),'-B',str(root/'project1/part2_experiment.py'),'--config',str(folder/'input.yaml'),'--output-dir',str(out),'--stage',stage]
if stage.startswith(('verify','fine')):
 bit=int(stage[-1]);delta=.0015 if stage.startswith('fine') else .003
 stop=float(sys.argv[3]) if len(sys.argv)>3 else .128
 args=[str(root/'.conda/python.exe'),'-B',str(run/'verify_candidate.py'),'--config',str(folder/'input.yaml'),'--structure',str(folder/'screen/part2_diagnostic.devsim'),'--output',str(out),'--bit',str(bit),'--delta',str(delta),'--stop-time',str(stop)]
else:
 if stage!='screen': args+=['--reload-structure',str(folder/'screen/part2_diagnostic.devsim')]
 if len(sys.argv)>3: args+=['--retention-delta-v',sys.argv[3]]
env=os.environ.copy();env['PATH']=str(root/'.conda/Library/bin')+os.pathsep+str(root/'.conda')+os.pathsep+env.get('PATH','');env['PYTHONIOENCODING']='utf-8'
deadline=datetime.datetime.fromisoformat(json.loads((run/'session.json').read_text())['deadline_utc'])
remaining=(deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds()
if remaining<120: raise RuntimeError('Insufficient remaining budget')
start=time.monotonic()
with log.open('xb') as stream:
 try:
  p=subprocess.run(args,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=remaining-90)
  result={'returncode':p.returncode,'elapsed_s':time.monotonic()-start,'command':args}
 except subprocess.TimeoutExpired:
  result={'timeout':True,'elapsed_s':time.monotonic()-start,'command':args}
(folder/(stage+'_process.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'label':label,'stage':stage,**result}),flush=True)
