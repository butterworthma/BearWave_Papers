"""Validate the published split and recompute summaries. Python 3 standard library."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import csv,hashlib,json,math
root=Path(__file__).resolve().parent
def read(path):
 with (root/path).open(newline='') as f:return list(csv.DictReader(f))
def quantile(v,p):
 v=sorted(v);k=(len(v)-1)*p;i=int(k);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(k-i)
def equal(a,b):assert math.isclose(float(a),float(b),abs_tol=1e-7), (a,b)
def checkstats(rows,table):
 for s in table:
  key=s['subset'];subset=[]
  for r in rows:
   prev=r['in_previous_spreadsheets'].lower()=='true';cq=r['category']=='CQ'
   keep={'all':True,'CQ_only':cq,'CQ_plus_HB':r['category'] in ['CQ','heartbeat'],'heartbeat_only':r['category']=='heartbeat','ID_only':r['category']=='ID_only','previous_selection':prev,'additional':not prev,'previous_CQ':prev and cq,'additional_CQ':not prev and cq}[key]
   if keep:subset.append(r)
  assert len(subset)==int(s['record_count'])
  for m in ['SNR_dB','DT_seconds']:
   v=[float(r[m]) for r in subset];assert len(v)==int(s[m+'_n'])
   for name,p in [('min',0),('q1',.25),('median',.5),('q3',.75),('max',1)]:
    if v:equal(s[m+'_'+name],quantile(v,p))
    else:assert s[m+'_'+name]==''
manifest=json.loads((root/'manifest.json').read_text())
for item in manifest['files']:
 assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
allrows=[]
for w in read('test_index.csv'):
 folder=Path(w['folder']);rows=read(folder/'received_records.csv');allrows+=rows
 assert len(rows)==int(w['RX_rows'])
 assert {r['window_id'] for r in rows}=={w['window_id']}
 assert {float(r['dial_frequency_MHz']) for r in rows}=={float(w['frequency_MHz'])}
 assert min(r['recorded_timestamp'] for r in rows)==w['first_UTC'][:19]
 assert max(r['recorded_timestamp'] for r in rows)==w['last_UTC'][:19]
 for label,key in [('CQ','CQ'),('heartbeat','HB'),('ID_only','ID')]:assert sum(r['category']==label for r in rows)==int(w[key])
 assert sum(r['in_previous_spreadsheets'].lower()=='true' for r in rows)==int(w['previous'])
 assert len(rows)-int(w['previous'])==int(w['additional'])
 checkstats(rows,read(folder/'descriptive_statistics.csv'))
 cq=sorted((r for r in rows if r['category']=='CQ'),key=lambda r:(r['recorded_timestamp'],r['record_id']))
 gaps=read(folder/'CQ_inter_reception_intervals.csv');assert len(gaps)==len(cq)-1
 values=[]
 for a,b,g in zip(cq,cq[1:],gaps):
  assert (g['previous_record_id'],g['next_record_id'])==(a['record_id'],b['record_id'])
  assert (g['previous_UTC'],g['next_UTC'])==(a['recorded_timestamp'],b['recorded_timestamp'])
  sec=(datetime.fromisoformat(b['recorded_timestamp'])-datetime.fromisoformat(a['recorded_timestamp'])).total_seconds();equal(g['gap_seconds'],sec);values.append(sec)
 st=read(folder/'CQ_spacing_summary.csv')[0];assert int(st['CQ_rows'])==len(cq) and int(st['intervals'])==len(values)
 freq=Counter(values);high=max(freq.values());assert int(st['mode_count_each'])==high
 modes=sorted(k for k,v in freq.items() if v==high);assert [float(x) for x in st['mode_seconds'].split(';')]==modes
 for name,p in [('min',0),('q1',.25),('median',.5),('q3',.75),('max',1)]:equal(st[name+'_seconds'],quantile(values,p))
assert len(allrows)==len({r['record_id'] for r in allrows})==1177
assert Counter(r['category'] for r in allrows)=={'CQ':1119,'heartbeat':25,'ID_only':33}
assert sum(r['in_previous_spreadsheets'].lower()=='true' for r in allrows)==484
checkstats(allrows,read('campaign_statistics.csv'))
print('PASS: hashes; 7 windows; 1,177 unique rows; 484 earlier + 693 additional; all SNR/DT summaries and CQ spacings reproduced.')
