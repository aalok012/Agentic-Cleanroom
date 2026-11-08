"""Read-only reconstruction of recorded labels, with explicit provenance and missing evidence.
Run from repo root. Does not reverify proofs or validate requirement satisfaction.
"""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path('/Users/alokthakur/Desktop/Research_ ADV(Shibbir)')
SOURCES = [BASE / n / 'outputs' for n in (
    'agentic-cleanroom copy', 'agentic-cleanroom', 'agentic-cleanroom MoT',
    'agentic-cleanroom MoT copy')]
OUT = ROOT / 'results/reviewer_audit'
LABELS = ['Proved', 'Proved-with-axioms', 'Tested', 'Uncertified',
          'Proof-assumptions-unknown', 'Evidence-missing']
AXIOM = re.compile(r'assume\s*\{:axiom\}')  # Match pipeline's recorded-label definition.
PAPER_SRS = {p.stem for p in (ROOT/'data/srs').glob('*.xml')}

def read(p):
    return json.loads(p.read_text())

def num(v):
    try: return float(v)
    except (ValueError, TypeError): return None

def close(a,b,tol=.011):
    return num(a) is not None and num(b) is not None and abs(float(a)-float(b))<=tol

def write_csv(name, rows):
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)

def log_blocks(path):
    data=read(path); m=data.get('metrics') or {}; loops=(data.get('recovery') or {}).get('loops') or []
    matching=[]
    for p in sorted(path.parent.glob('*.log')):
        text=p.read_text(errors='replace')
        for mark in re.finditer(r'total_time\s*:\s*([0-9.]+)s',text):
            if close(mark[1],m.get('total_seconds')):
                matching.append(text[:mark.end()])
    if not matching: return []
    alternatives=[]
    for text in matching:
        blocks=[]
        for part in text.split('TEST RESULTS')[1:]:
            header=part.split('SUMMARY:',1)
            if len(header)!=2: continue
            entries=re.findall(r'^[ \t]*\[(PASS|FAIL)\][ \t]+(\S+)[ \t]+sample=(\d+)[ \t]',header[0].split('=== FAILURES ===')[0],re.M)
            count=re.match(r'\s*(\d+) passed / (\d+) failed / (\d+) total case executions',header[1])
            if not count or len(entries)!=int(count[3]): continue
            if sum(e[0]=='PASS' for e in entries)!=int(count[1]): continue
            by_fr=defaultdict(list)
            for verdict,fr,sample in entries: by_fr[fr].append(verdict=='PASS')
            blocks.append(dict(by_fr))
        if len(blocks)>=1+len(loops): alternatives.append(blocks[-(1+len(loops)):])
    if not alternatives:return []
    if len({json.dumps(x,sort_keys=True) for x in alternatives})>1:return []
    return alternatives[0]

def signature(d):
    # Disregard machine paths, timings and raw source formatting; compare label evidence.
    feats=d.get('generated_dafny',{}).get('features',[])
    return json.dumps({'features':d.get('features'),
        'proofs':[(x['feature_id'],x.get('verified'),x.get('axioms')) for x in feats],
        'proved':d.get('proved_feature_ids'), 'cert':d.get('certification'),
        'recovery':d.get('recovery')},sort_keys=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    candidates=[]; index=defaultdict(list); inventory=[]
    for source in SOURCES:
        full=sorted(source.rglob('*_full_ir.json'))
        inventory.append({'root':str(source),'full_ir':len(full),
                          'recovery_logs':len(list(source.rglob('*_recovery_iters.jsonl')))})
        for p in full:
            try: d=read(p)
            except (ValueError,OSError): continue
            c={'path':p,'d':d,'m':d.get('metrics') or {}}
            candidates.append(c)
            for rp in (p.parent/'runs').glob('*.json'):
                try: rec=read(rp)
                except (ValueError,OSError): continue
                # Only associate a full IR with the exact run it represents, not a stale sibling.
                if (rec.get('tokens')==c['m'].get('tokens') and
                    close(rec.get('total_seconds'),c['m'].get('total_seconds'))):
                    index[rp.stem].append(c)
    requests=[]
    for filename,cohort in [('experiment_metrics.csv','RQ1_archive'),
                            ('newmodels_metrics_current.csv','newmodels_archive'),
                            ('cot_deepseek_results.csv','CoT'),('mot_deepseek_results.csv','MoT')]:
        for i,row in enumerate(csv.DictReader((ROOT/'results/raw_results'/filename).open())):
            requests.append((filename,cohort,i+2,row))
    matches=[]; fr_rows=[]; run_rows=[]
    for filename,cohort,line,row in requests:
        match={'archive':filename,'csv_line':line,'cohort':cohort,
               'run_id':row.get('run_id',''),'srs':row['srs'],'language':row['language'],
               'model':row.get('model','deepseek/deepseek-v3.2')}
        if row.get('status','complete')!='complete':
            matches.append({**match,'status':'excluded_failed_run'});continue
        possible=[]
        pool=index.get(row['run_id'],[]) if row.get('run_id') else candidates
        for c in pool:
            m=c['m'];d=c['d'];s=m.get('summary') or {}
            if Path(m.get('srs','')).stem!=row['srs']:continue
            if (m.get('language') or d.get('language') or m.get('config',{}).get('language'))!=row['language']:continue
            if row.get('run_id'):
                if not close(m.get('tokens',{}).get('total'),row.get('tokens_total'),0):continue
                if not close(m.get('total_seconds'),row.get('total_seconds')):continue
            else:
                if m.get('config',{}).get('prompt_strategy')!=cohort.lower():continue
                if not close(m.get('tokens',{}).get('total'),row.get('total_tokens'),0):continue
                if not close(s.get('total_time'),row.get('total_time')):continue
            if any(not close(s.get(k),row[k],.00011) for k in ['verification_pass_ratio','PassVer@1'] if row.get(k)):continue
            possible.append(c)
        if not possible:
            matches.append({**match,'status':'no_exact_artifact_match'});continue
        sigs={signature(c['d']) for c in possible}
        if len(sigs)>1:
            matches.append({**match,'status':'conflicting_label_evidence','candidates':len(possible)});continue
        def quality(x):
            lp=x['path'].parent/'run.log'
            times=re.findall(r'total_time\s*:\s*([0-9.]+)s',lp.read_text(errors='replace')) if lp.exists() else []
            return (len(log_blocks(x['path'])), bool(times and close(times[-1],x['m'].get('total_seconds'))))
        c=max(possible,key=quality)
        p,d,m=c['path'],c['d'],c['m'];rec=d.get('recovery') or {};loops=rec.get('loops') or []
        matches.append({**match,'status':'matched','copies':len(possible),'full_ir':str(p),
                        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        mapping={str(f['id']):[str(r['id']) for r in f.get('functional_requirements',[])] for f in d['features']}
        all_fr=[r for ids in mapping.values() for r in ids]
        if len(all_fr)!=len(set(all_fr)): raise ValueError('Duplicate FR IDs: '+str(p))
        initial_proofs={str(f['feature_id']):f for f in (d.get('generated_dafny') or {}).get('features',[])}
        initial_proved={fid for fid,f in initial_proofs.items() if f.get('verified')}
        final_proved=set(map(str,m.get('proved_feature_ids',rec.get('proved_feature_ids',d.get('proved_feature_ids',initial_proved)))))
        cert=d.get('certification') or {}
        final_tests={str(f['fr_id']):f for f in cert.get('frs',[])}
        blocks=log_blocks(p)
        # Logs should contain the initial pass plus one pass per completed recovery loop.
        log_ok=len(blocks)==1+len(loops)
        if log_ok:
            last_pass={r for r,v in blocks[-1].items() if v and all(v)}
            cert_pass={r for r,f in final_tests.items() if f.get('pass_at',{}).get('pass@1',0)>=1}
            log_ok=last_pass==cert_pass and set(blocks[-1])==set(final_tests)
        initial_tests=blocks[0] if log_ok else None
        byproof=set(map(str,rec.get('repaired_by_proof',[])))
        bytests=set(map(str,rec.get('repaired_by_tests',[])))
        common={**match,'full_ir':str(p),'paper_subject':row['srs'] in PAPER_SRS,
                'paper_model':match['model']!='openai_gpt-4_1',
                'configured_model':m.get('config',{}).get('models',{}).get('code',''),
                'actual_models':m.get('model',''),'oracle':cert.get('oracle',''),
                'recovery_loops':len(loops),'initial_log_validated':log_ok}
        for fid,ids in mapping.items():
            for fr in ids:
                item={**common,'feature_id':fid,'fr_id':fr}
                for phase,proved in [('initial',initial_proved),('final',final_proved)]:
                    label='Evidence-missing';evidence=''
                    if fid in proved:
                        f=initial_proofs.get(fid,{})
                        if phase=='initial' or fid in initial_proved:
                            ax=f.get('axioms')
                            if ax is not None:
                                label='Proved-with-axioms' if ax else 'Proved';evidence='generated_dafny verified + recorded axioms'
                            else:label='Proof-assumptions-unknown'
                        else:
                            module=f.get('module','F'+re.sub(r'[^0-9A-Za-z]','_',fid))
                            sources=list((p.parent/'generated').glob('*/dafny_proof/dafny/'+module+'.dfy'))
                            log_text=(p.parent/'run.log').read_text(errors='replace') if (p.parent/'run.log').exists() else ''
                            times=re.findall(r'total_time\s*:\s*([0-9.]+)s',log_text)
                            stale_source=bool(times and not close(times[-1],m.get('total_seconds')))
                            if len(sources)==1 and not stale_source:
                                label='Proved-with-axioms' if AXIOM.search(sources[0].read_text()) else 'Proved'
                                evidence='final proved ID + archived recovery source scan: '+str(sources[0])
                            else:label='Proof-assumptions-unknown'
                    elif phase=='final' or not loops:
                        f=final_tests.get(fr)
                        if f and f.get('n_test_cases',0)>0:
                            label='Tested' if f.get('pass_at',{}).get('pass@1',0)>=1 else 'Uncertified'
                            evidence='certification.frs'
                        else:
                            label='Uncertified';evidence='no passing test evidence for FR' if cert else 'certification absent; no test certification recorded'
                    elif initial_tests is not None:
                        v=initial_tests.get(fr,[])
                        label='Tested' if v and all(v) else 'Uncertified';evidence='initial run.log certification block'
                    item[phase+'_label']=label;item[phase+'_evidence']=evidence
                item['recovery_feature_flag']='proof' if fid in byproof else 'tests' if fid in bytests else ''
                item['newly_certified']=item['initial_label']=='Uncertified' and item['final_label'] in ('Proved','Proved-with-axioms','Proof-assumptions-unknown','Tested')
                fr_rows.append(item)
        current=[x for x in fr_rows if x['archive']==filename and x['csv_line']==line]
        summary={**common,'total_frs':len(current),'copies':len(possible)}
        for phase in ['initial','final']:
            counts=Counter(x[phase+'_label'] for x in current)
            for label in LABELS:summary[phase+'_'+label]=counts[label]
            assert sum(counts.values())==len(all_fr)
        summary['newly_certified']=sum(x['newly_certified'] for x in current)
        summary['newly_certified_by_proof']=sum(x['newly_certified'] and x['final_label'] in ('Proved','Proved-with-axioms','Proof-assumptions-unknown') for x in current)
        summary['newly_certified_by_tests']=sum(x['newly_certified'] and x['final_label']=='Tested' for x in current)
        summary['recovery_flagged_frs']=sum(bool(x['recovery_feature_flag']) for x in current)
        vpr=sum(x['final_label'] in ('Proved','Proved-with-axioms','Proof-assumptions-unknown') for x in current)/len(current)
        pv=sum(x['final_label'] in ('Proved','Proved-with-axioms','Proof-assumptions-unknown','Tested') for x in current)/len(current)
        summary['VPR_reconstructed']=vpr;summary['PassVer_reconstructed']=pv
        summary['VPR_matches_archive']=close(vpr,row.get('verification_pass_ratio'),.00011)
        summary['PassVer_matches_archive']=close(pv,row.get('PassVer@1'),.00011)
        run_rows.append(summary)
    write_csv('artifact_matches.csv',matches);write_csv('per_requirement_labels.csv',fr_rows);write_csv('per_run_counts.csv',run_rows)
    # Keep cohorts and version identifiers separate; no averaging unequal populations silently.
    grouped=defaultdict(list)
    for r in fr_rows:
        if r['paper_subject'] and r['paper_model']:grouped[(r['cohort'],r['model'],r['language'])].append(r)
    aggregates=[]
    for (cohort,model,language),rs in sorted(grouped.items()):
        for phase in ['initial','final']:
            counts=Counter(r[phase+'_label'] for r in rs)
            a={'cohort':cohort,'model':model,'language':language,'phase':phase,
               'runs':len({r['csv_line'] for r in rs}),'subjects':len({r['srs'] for r in rs}),
               'total_requirement_instances':len(rs)}
            for label in LABELS:a[label]=counts[label];a[label+'_pct']=round(100*counts[label]/len(rs),2)
            a['initial_evidence_missing']=sum(r['initial_label']=='Evidence-missing' for r in rs)
            a['newly_certified_after_recovery']=sum(r['newly_certified'] for r in rs) if phase=='final' else ''
            aggregates.append(a)
    write_csv('per_setting_counts.csv',aggregates)
    report={'inventory':inventory,'match_status':dict(Counter(r['status'] for r in matches)),
            'matched_by_cohort':dict(Counter(r['cohort'] for r in run_rows)),
            'VPR_mismatches':sum(not r['VPR_matches_archive'] for r in run_rows),
            'PassVer_mismatches':sum(not r['PassVer_matches_archive'] for r in run_rows),
            'missing_initial_FRs':sum(r['initial_label']=='Evidence-missing' for r in fr_rows),
            'unknown_final_axioms':sum(r['final_label']=='Proof-assumptions-unknown' for r in fr_rows)}
    lines=['# Reviewer label-distribution audit','',
        'Reconstruction of recorded pipeline evidence; this is not a human faithfulness audit or new execution of generated applications.','',
        '## Scope and matching','',
        '- Matched 138 completed RQ1 archive rows, 20 new-model archive rows, and 30 rows each for CoT and MoT. The 20 new-model rows also occur in the RQ1 archive; never add these cohorts together.',
        '- One failed RQ1 row is excluded and retained in artifact_matches.csv.',
        '- Matching uses archived run IDs, token totals, time, language, subject, VPR and PassVer@1; prompting cohorts additionally match strategy. Equivalent copies count once within each cohort.',
        '- Per-setting tables restrict subjects to the ten XML files in the current benchmark. Extra subjects and the extra GPT-4.1 model remain in per-run/per-requirement exports for traceability, but are excluded from per-setting tables.',
        '- This yields 125 completed RQ1 rows for the ten paper subjects, not a balanced 180-cell matrix. DeepSeek version identifiers are kept separate. Exact Table I inclusion/weighting still needs confirmation; these are available-archive distributions, not a claimed reproduction of Table I.',
        '- Counts below pool requirement instances across runs; they are not unique source requirements or macro-averaged VPR.','',
        '## Available RQ1 archive: ten paper subjects','',
        '| Evidence | Before recovery | Final |','|---|---:|---:|']
    rq=[r for r in run_rows if r['cohort']=='RQ1_archive' and r['paper_subject'] and r['paper_model']]
    for label in LABELS:
        lines.append('| '+label+' | '+str(sum(r['initial_'+label] for r in rq))+' | '+str(sum(r['final_'+label] for r in rq))+' |')
    lines+=['| Total requirement instances | '+str(sum(r['total_frs'] for r in rq))+' | '+str(sum(r['total_frs'] for r in rq))+' |','',
        'Confirmed newly certified requirement instances: '+str(sum(r['newly_certified'] for r in rq))+'. This is a lower bound when initial evidence is missing. Repaired is a transition/provenance flag, not a fifth mutually exclusive final label.','',
        '## Model-language breakdown (final RQ1 archive)','',
        '| Archived model identifier | Language | Subjects | FR instances | Proved | With axioms | Proof assumptions unknown | Tested (recorded) | Uncertified |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for a in aggregates:
        if a['cohort']=='RQ1_archive' and a['phase']=='final':
            lines.append('| '+' | '.join(str(a[k]) for k in ['model','language','subjects','total_requirement_instances','Proved','Proved-with-axioms','Proof-assumptions-unknown','Tested','Uncertified'])+' |')
    lines+=['','## Evidence limits','',
        '- Initial test outcomes are recovered from log blocks anchored to the matched run duration; case totals and final FR verdicts are checked against structured certification. Missing initial outcomes remain unknown, not zero.',
        '- Initial proof outcomes and axiom lists come from generated_dafny. Final proved IDs prefer metrics/recovery because older top-level IDs can remain stale.',
        '- For newly proved recovery features, axiom status is inferred from the archived final Dafny source using the pipeline’s assume {:axiom} pattern. Where logs show later runs that may have overwritten the source, the split is unknown. This is recorded-label reconstruction, not a complete audit of all ways Dafny can trust assumptions.',
        '- Uncertified includes failed cases, omitted tests and absent certification. In two Haiku FoodSaver runs (Java/Python), no certification result is saved; their remaining requirements carry no test evidence.',
        '- Java/Spring recorded test passes represent compilation checks in the inspected implementation, not executed behavioral tests. The per-requirement file retains oracle names; do not present those counts as validated runtime satisfaction.',
        '- Proof is feature-level and credits all contained FRs, following the original metric; this does not independently establish per-FR proof adequacy.','',
        '## Outstanding evidence gaps','',
        '| Cohort | Subject | Model | Language | Missing initial FRs | Final proof axiom split unknown |','|---|---|---|---|---:|---:|']
    for r in run_rows:
        if r['initial_Evidence-missing'] or r['final_Proof-assumptions-unknown']:
            lines.append('| '+' | '.join(str(r[k]) for k in ['cohort','srs','model','language','initial_Evidence-missing','final_Proof-assumptions-unknown'])+' |')
    lines+=['','## Files','',
        '- per_setting_counts.csv: counts and percentages by cohort/model/language, before and after recovery.',
        '- per_run_counts.csv: subject-level counts and metric consistency checks.',
        '- per_requirement_labels.csv: individual labels, transitions, source paths and evidence.',
        '- artifact_matches.csv: source CSV row, matching artifact path, duplicate count and SHA-256.',
        '- audit_summary.json: matching and validation totals.','',
        'Reproduce: `python3 scripts/audit_label_distributions.py`. Source roots are explicitly listed at the top of that script.']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n')
    (OUT/'audit_summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
