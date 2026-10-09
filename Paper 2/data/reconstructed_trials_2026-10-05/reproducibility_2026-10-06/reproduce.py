"""Recompute and validate the Paper 2 numerical results. Python 3.10+, standard library.

Run: python3 reproduce.py --output results
Inputs and expected results are read-only. Output is separate. No network access is used.
"""
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import argparse, csv, hashlib, json, math, re, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parent
CHECKS=[]
def read(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
    if not rows:raise ValueError(f'Empty output: {path.name}')
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def require(ok,label):
    if not ok:raise ValueError(label)
def check(ok,label):
    require(ok,label);CHECKS.append(label)
def same(a,b):
    if a in ('',None) or b in ('',None):return a in ('',None) and b in ('',None)
    try:return math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-7)
    except (TypeError,ValueError):return str(a)==str(b)
def compare(rows,path,keys):
    expected=read(path)
    def keyed(data):return {tuple(str(r[k]) for k in keys):r for r in data}
    a,b=keyed(rows),keyed(expected)
    require(len(a)==len(rows) and len(b)==len(expected),'Duplicate comparison keys: '+path.name)
    require(a.keys()==b.keys(),'Row keys differ: '+path.name)
    for key,row in b.items():
        for k,v in row.items():require(k in a[key] and same(a[key][k],v),f'{path.name}: {key}: {k}: {a[key].get(k)} != {v}')
    CHECKS.append('Reproduced '+path.name)
def quantile(values,p):
    v=sorted(values)
    if not v:return None
    k=(len(v)-1)*p;i=int(k);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(k-i)
def stats(values):return dict(zip(['min','q1','median','q3','max'],[quantile(values,p) for p in [0,.25,.5,.75,1]]))
def timestamp(text):return datetime.fromisoformat(text)
def subsets(r):
    cq=r['category']=='CQ';prev=r['in_previous_spreadsheets'].lower()=='true'
    return {'all':True,'CQ_only':cq,'CQ_plus_HB':r['category'] in ['CQ','heartbeat'],
            'heartbeat_only':r['category']=='heartbeat','ID_only':r['category']=='ID_only',
            'previous_selection':prev,'additional':not prev,'previous_CQ':prev and cq,'additional_CQ':not prev and cq}

def reception_analysis(out):
    rows=read(ROOT/'inputs/receptions.csv');rules=read(ROOT/'inputs/window_rules.csv')
    check(len(rows)==len({r['record_id'] for r in rows})==1177,'Unique reception inventory: 1177 rows')
    for r in rows:
        assigned=[w['window'] for w in rules if float(w['frequency_MHz'])==float(r['dial_frequency_MHz']) and w['UTC_date_inclusive']<=r['recorded_timestamp'][:10]<w['UTC_date_exclusive']]
        require(assigned==[r['window_id']], 'Window rule mismatch: '+r['record_id'])
        require(all(math.isfinite(float(r[k])) for k in ['SNR_dB','DT_seconds']),'Invalid numeric reception')
    CHECKS.append('All reception rows assigned exactly once by frequency/date rules, with no SNR filtering')
    groups={w:[] for w in ['W1','W2','W3','W4','W5','W6','W7']}
    for r in rows:groups[r['window_id']].append(r)
    frequencies=sorted({r['dial_frequency_MHz'] for r in rows},key=float)
    scopes=[('campaign',rows)]+list(groups.items())+[(f'{float(f):.3f}MHz_pooled',[r for r in rows if r['dial_frequency_MHz']==f]) for f in frequencies]
    summaries=[]
    for scope,items in scopes:
        for key in subsets(rows[0]):
            a=[r for r in items if subsets(r)[key]];d={'scope':scope,'subset':key,'record_count':len(a)}
            for metric in ['SNR_dB','DT_seconds']:
                v=[float(r[metric]) for r in a];d[metric+'_n']=len(v)
                d.update({metric+'_'+k:v for k,v in stats(v).items()})
            summaries.append(d)
    compare(summaries,ROOT/'expected/descriptive_summaries.csv',['scope','subset'])
    write(out/'descriptive_summaries.csv',summaries)
    intervals,gapstats,coverage,counts=[],[],[],[]
    for w,items in groups.items():
        cq=sorted((r for r in items if r['category']=='CQ'),key=lambda r:(r['recorded_timestamp'],r['record_id']))
        gaps=[]
        for a,b in zip(cq,cq[1:]):
            gap=int((timestamp(b['recorded_timestamp'])-timestamp(a['recorded_timestamp'])).total_seconds());gaps.append(gap)
            intervals.append({'window_id':w,'previous_record_id':a['record_id'],'next_record_id':b['record_id'],
                              'previous_UTC':a['recorded_timestamp'],'next_UTC':b['recorded_timestamp'],'gap_seconds':gap})
        c=Counter(gaps);n=max(c.values());modes=sorted(k for k,v in c.items() if v==n)
        gapstats.append({'window_id':w,'CQ_rows':len(cq),'intervals':len(gaps),'mode_seconds':';'.join(map(str,modes)),
                         'mode_count_each':n,**{k+'_seconds':v for k,v in stats(gaps).items()}})
        prev=sum(r['in_previous_spreadsheets'].lower()=='true' for r in items)
        coverage.append({'window_id':w,'frequency_MHz':items[0]['dial_frequency_MHz'],
                         'first_UTC':min(r['recorded_timestamp'] for r in items)+'+00:00',
                         'last_UTC':max(r['recorded_timestamp'] for r in items)+'+00:00','RX_rows':len(items),
                         'CQ':len(cq),'HB':sum(r['category']=='heartbeat' for r in items),
                         'ID':sum(r['category']=='ID_only' for r in items),'previous':prev,'additional':len(items)-prev})
    for name,data,keys in [('CQ_gap_summaries.csv',gapstats,['window_id']),('CQ_inter_reception_intervals.csv',intervals,['window_id','previous_record_id','next_record_id']),('window_coverage.csv',coverage,['window_id'])]:
        compare(data,ROOT/'expected'/name,keys);write(out/name,data)
    for f in frequencies:
        a=[r for r in rows if r['dial_frequency_MHz']==f]
        counts.append({'frequency_MHz':f,'test':sum(r['category']=='CQ' for r in a),'heartbeat':sum(r['category']=='heartbeat' for r in a),'ID_only':sum(r['category']=='ID_only' for r in a),'total':len(a)})
    write(out/'frequency_counts.csv',counts)
    bins=defaultdict(list)
    for r in rows:
        if r['category']=='CQ':
            t=timestamp(r['recorded_timestamp'])+timedelta(hours=8)
            bins[(r['window_id'],str(t.date()),t.hour//4*4)].append(float(r['SNR_dB']))
    snr=[{'window':w,'local_date':d,'local_hour_start':h,'n':len(v),'median_SNR_dB':quantile(v,.5),'min_SNR_dB':min(v),'max_SNR_dB':max(v)} for (w,d,h),v in sorted(bins.items())]
    compare(snr,ROOT/'expected/SNR_by_local_time.csv',['window','local_date','local_hour_start']);write(out/'SNR_by_local_time.csv',snr)
    longest=max(intervals,key=lambda r:r['gap_seconds'])
    check(longest['gap_seconds']==24945 and longest['previous_UTC']=='2023-04-17 13:52:45','Longest within-window test interval: 24945 seconds')
    one_w=[];matched_points=[]
    for chart in ['chart1.xml','chart3.xml','chart4.xml']:
        points=[r for r in read(ROOT/'inputs/nominal_power_chart_points.csv') if r['chart']==chart]
        matched=[]
        for p in points:
            hits=[r for r in rows if r['recorded_timestamp']==p['recorded_timestamp'] and same(r['dial_frequency_MHz'],p['frequency_MHz']) and same(r['SNR_dB'],p['SNR_dB'])]
            require(len(hits)==1,'Power-chart point lacks a unique reception match: '+str(p))
            matched.append(hits[0]);matched_points.append({**p,'record_id':hits[0]['record_id'],'window':hits[0]['window_id']})
        require(len({r['window_id'] for r in matched})==1,'Power chart spans different windows')
        one_w.append({'window':matched[0]['window_id'],'frequency_MHz':matched[0]['dial_frequency_MHz'],'receptions':len(matched),
                      'basis':'Unique timestamp/frequency/SNR matches to '+chart+'; nominal 1 W from chart/report, not a per-reception power measurement'})
    check([r['receptions'] for r in one_w]==[126,102,92],'Nominal 1 W subset counts reproduced; configuration basis remains documentary')
    write(out/'nominal_1W_subsets.csv',one_w)
    write(out/'nominal_1W_record_mapping.csv',matched_points)
    return rows,summaries,longest

def map_analysis(rows,out):
    palette={tuple(int(r[k]) for k in ['red','green','blue']):int(r['class_MHz']) for r in read(ROOT/'inputs/map_palette.csv')}
    pixels=defaultdict(list)
    for p in read(ROOT/'inputs/map_pixels.csv'):
        pixels[p['filename']].append((int(p['dx']),int(p['dy']),tuple(int(p[k]) for k in ['red','green','blue'])))
    stations={}
    for station in ['Darwin','Guam']:
        vals=read(ROOT/f'inputs/{station}_2023_foF2.csv')
        stations[station]={datetime(2023,4,1)+timedelta(seconds=round((float(r['April_day'])-1)*86400)):float(r['foF2_MHz']) for r in vals}
        check(len(vals)==len(stations[station])==1344,station+' series: 1344 unique quarter-hour observations')
        compare(vals,ROOT/f'figures/{station}_2023_foF2.csv',['April_day'])
    classes=[]
    for item in read(ROOT/'inputs/map_inventory.csv'):
        r=dict(item);t=timestamp(r['timestamp_UTC']);a=pixels[r['filename']]
        require(len(a)==len({(x,y) for x,y,c in a})==49,'Map pixel patch incomplete')
        for radius in [1,2,3]:
            v=[palette[c] for x,y,c in a if abs(x)<=radius and abs(y)<=radius and c in palette]
            counts=Counter(v).most_common()
            mode=counts[0][0] if counts and (len(counts)==1 or counts[0][1]>counts[1][1]) else None
            r.update({f'r{radius}_mode':mode,f'r{radius}_min':min(v) if v else None,f'r{radius}_max':max(v) if v else None,f'r{radius}_pixels':len(v)})
        local=t+timedelta(hours=8);r['local_hour']=local.hour;r['local_date']=str(local.date())
        for station,series in stations.items():r[station+'_foF2_MHz']=series.get(t)
        classes.append(r)
    compare(classes,ROOT/'expected/Map_colour_classes.csv',['filename']);write(out/'Map_colour_classes.csv',classes)
    lookup={timestamp(r['timestamp_UTC']):r for r in classes};joined=[]
    for r in rows:
        t=timestamp(r['recorded_timestamp']);grid=t.replace(minute=t.minute//15*15,second=0)
        if t-grid>timedelta(seconds=450):grid+=timedelta(minutes=15)
        m=lookup.get(grid)
        if not m:continue
        d={k:r[k] for k in ['record_id','recorded_timestamp','dial_frequency_MHz','SNR_dB','category','window_id']}
        d.update({k:v for k,v in m.items() if k!='sha256'});d['map_minus_receive_seconds']=(grid-t).total_seconds()
        for radius in [1,2,3]:
            v=m[f'r{radius}_mode'];f=float(r['dial_frequency_MHz'])
            d[f'r{radius}_mode_comparison_1MHz_buffer']='unresolved' if v is None else 'below' if f<v-1 else 'above' if f>v+1 else 'near'
        joined.append(d)
    compare(joined,ROOT/'expected/Matched_receptions.csv',['record_id']);write(out/'Matched_receptions.csv',joined)
    hourly=[]
    for hour in range(24):
        a=[r['r2_mode'] for r in classes if r['local_hour']==hour and '2023-04-15'<=r['local_date']<='2023-04-20' and r['r2_mode'] is not None]
        st=stats(a);hourly.append({'local_hour':hour,'maps':len(a),**{k+'_class':v for k,v in st.items()}})
    compare(hourly,ROOT/'expected/Hourly_map_summary.csv',['local_hour']);write(out/'Hourly_map_summary.csv',hourly)
    blocks=[]
    for radius in [1,2,3]:
        for label,hours in [('04-06',range(4,7)),('10-17',range(10,18)),('18-23',range(18,24))]:
            a=[r[f'r{radius}_mode'] for r in classes if r['local_hour'] in hours and '2023-04-15'<=r['local_date']<='2023-04-20' and r[f'r{radius}_mode'] is not None]
            blocks.append({'patch_size':2*radius+1,'local_hours':label,'maps':len(a),'median_class_MHz':quantile(a,.5),'min_class_MHz':min(a),'max_class_MHz':max(a)})
    check(all(r['median_class_MHz']==(7 if r['local_hours']=='04-06' else 11) for r in blocks),'Mapped dawn/day/evening medians reproduced for all three patch sizes')
    write(out/'map_daily_blocks.csv',blocks)
    missing=[];t=min(lookup)
    while t<=max(lookup):
        if t not in lookup:missing.append({'timestamp_UTC':str(t)})
        t+=timedelta(minutes=15)
    check(len(classes)==667 and len(missing)==12,'Map coverage: 667 inputs, 12 missing scheduled maps')
    write(out/'missing_map_times.csv',missing)
    summary={'maps':len(classes),'matched_receptions':len(joined),'matched_test_receptions':sum(r['category']=='CQ' for r in joined),
             'unresolved_modes':{str(2*k+1):sum(r[f'r{k}_mode'] is None for r in classes) for k in [1,2,3]},
             'first_map_UTC':str(min(lookup)),'last_map_UTC':str(max(lookup)),
             'station_ranges_MHz':{s:[min(v.values()),max(v.values())] for s,v in stations.items()}}
    (out/'map_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

def chamber_analysis(out):
    rows=[]
    pattern=r"^(\d{2}:\d{2}:\d{2})\s+([\d.]+)'C\s+(\d+)MHz\s+(\d+)MHz\s+([01]+)\s+([\d.]+)V$"
    lines=(ROOT/'inputs/chamber_pi_results.txt').read_text().splitlines()
    for n,line in enumerate(lines[1:],2):
        if not line.strip() or line.split()==['Time','Temp','CPU','Core','Health','Vcore']:continue
        m=re.fullmatch(pattern,line.strip());require(m is not None,f'Unparsed diagnostic row {n}')
        t,temp,cpu,core,health,voltage=m.groups();bits=int(health,2)
        rows.append({'source_line':n,'recorded_time':t,'temperature_C':float(temp),'CPU_MHz':int(cpu),'core_MHz':int(core),
                     'health_bits':health,'Vcore_V':float(voltage),'undervoltage_current':int(bool(bits&1)),
                     'throttled_current':int(bool(bits&4)),'undervoltage_history':int(bool(bits&(1<<16))),
                     'throttled_history':int(bool(bits&(1<<18)))})
    summary={'rows':len(rows),'temperature_min_C':min(r['temperature_C'] for r in rows),'temperature_max_C':max(r['temperature_C'] for r in rows),
             'health_counts':dict(Counter(r['health_bits'] for r in rows)),'time_zone':'Unspecified; times preserved as recorded',
             'date':'2023-10-26, author supplied','chamber_setpoint_C':30,'setpoint_stability_C':0.1,'chamber_temperature_source':'Author account, not a chamber-logger time series'}
    check(len(rows)==1930 and summary['temperature_min_C']==58.4 and summary['temperature_max_C']==75.0,'Pi diagnostic: 1930 records and 58.4–75.0 C range')
    write(out/'chamber_pi_records.csv',rows);(out/'chamber_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

def validate_figures(summaries,out):
    lookup={(r['scope'],r['subset']):r for r in summaries}
    expected=[]
    for metric in ['SNR_dB','DT_seconds']:
        for i in range(1,8):
            a=lookup[(f'W{i}','all')];q=lookup[(f'W{i}','CQ_only')]
            expected += [[(i-.12,a[metric+'_min']),(i-.12,a[metric+'_max'])],
                         [(i-.12,a[metric+'_q1']),(i-.12,a[metric+'_q3'])],[(i-.12,a[metric+'_median'])],
                         [(i+.12,q[metric+'_q1']),(i+.12,q[metric+'_q3'])],[(i+.12,q[metric+'_median'])]]
    text=(ROOT/'figures/window_distributions.tex').read_text()
    matches=list(re.finditer(r'coordinates \{([^}]+)\}',text))
    require(len(matches)==len(expected),'Unexpected number of distribution-plot coordinates')
    for m,coords in zip(matches,expected):
        actual=[tuple(map(float,p)) for p in re.findall(r'\(([-\d.]+),([-\d.]+)\)',m.group(1))]
        require(len(actual)==len(coords) and all(same(a,b) for p,q in zip(actual,coords) for a,b in zip(p,q)),'Distribution figure differs from recomputed summaries')
    CHECKS.append('Every distribution-figure coordinate matches recomputed SNR/DT statistics')
    folder=out/'figures';folder.mkdir(exist_ok=True)
    for p in (ROOT/'figures').iterdir():shutil.copy2(p,folder/p.name)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=ROOT/'results');args=ap.parse_args()
    out=args.output.resolve()
    require(out not in [ROOT,ROOT/'inputs',ROOT/'expected',ROOT/'baseline_release'],'Choose a separate output directory')
    for protected in ['inputs','expected','baseline_release','figures']:
        require(not out.is_relative_to(ROOT/protected),'Output must not be inside '+protected)
    out.mkdir(parents=True,exist_ok=True)
    # A failed rerun must not leave a previous PASS report looking current.
    (out/'validation.json').unlink(missing_ok=True)
    manifest=ROOT/'manifest.json'
    require(manifest.exists(),'Package manifest is missing')
    if manifest.exists():
        for item in json.loads(manifest.read_text())['files']:
            require(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],'File hash differs: '+item['path'])
        CHECKS.append('Package source and expected-result hashes verified')
    subprocess.run([sys.executable,str(ROOT/'baseline_release/verify_results.py')],check=True,capture_output=True,text=True)
    CHECKS.append('Published baseline verifier passes with the manifest-matching missing .gitignore restored locally')
    rows,summaries,longest=reception_analysis(out)
    maps=map_analysis(rows,out);chamber=chamber_analysis(out);validate_figures(summaries,out)
    report={'status':'PASS','protocol':'1.3 retrospective amendment','python':sys.version.split()[0],
            'checks':CHECKS,'reception_count':len(rows),'longest_within_window_interval':longest,'ionosphere':maps,
            'chamber':chamber,'boundaries':['Reception statistics start from processed public receive rows; raw-log parsing/deduplication is not rerun.',
            'Map classifications start from included original RGB patches; optional extract_sources.py re-extracts from original PNGs.',
            'Configuration and welfare/energy targets are documentary or design inputs, not inferred from successful reception.']}
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {len(CHECKS)} checks; 1177 receptions; 667 maps; 1930 Pi records. Results: {out}')

if __name__=='__main__':main()
