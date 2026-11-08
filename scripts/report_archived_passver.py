"""Reconstruct final RQ1 archive PassVer@1; do not infer Table I membership."""
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/reviewer_audit'


def main():
    with (OUT / 'per_run_counts.csv').open() as source:
        rows = [r for r in csv.DictReader(source)
                if r['cohort'] == 'RQ1_archive'
                and r['paper_subject'] == 'True' and r['paper_model'] == 'True']
    groups = defaultdict(list)
    runs = []
    for r in rows:
        d = json.loads(Path(r['full_ir']).read_text())
        metrics = d['metrics']
        features = {str(f['id']): {str(q['id']) for q in f['functional_requirements']}
                    for f in d['features']}
        universe = set().union(*features.values())
        proved_features = metrics.get('proved_feature_ids')
        if proved_features is None:
            proved_features = d.get('proved_feature_ids', [])
        proved = set().union(*(features[str(fid)] for fid in proved_features))
        tested = set(metrics.get('certification', {}).get('pass_at_1_fr_ids', []))
        assert proved | tested <= universe
        certified = proved | tested
        ratio = len(certified) / len(universe)
        assert len(universe) == int(r['total_frs'])
        assert abs(ratio - float(r['PassVer_reconstructed'])) < 0.00011
        assert abs(ratio - float(metrics['summary']['PassVer@1'])) < 0.00011
        conservative = sum(int(r['final_' + label])
                           for label in ['Proved', 'Proved-with-axioms', 'Tested'])
        run = dict(run_id=r['run_id'], model=r['model'], language=r['language'],
                   srs=r['srs'], full_ir=r['full_ir'], total=len(universe),
                   proved=len(proved), test_passing=len(tested), overlap=len(proved & tested),
                   certified=len(certified), passver=ratio,
                   conservative_certified=conservative,
                   conservative_passver=conservative / len(universe),
                   oracle=r['oracle'], recovery_loops=int(r['recovery_loops']))
        runs.append(run)
        groups[r['model'], r['language']].append(run)
    settings = []
    for (model, language), items in sorted(groups.items()):
        n = sum(x['total'] for x in items)
        c = sum(x['certified'] for x in items)
        conservative = sum(x['conservative_certified'] for x in items)
        settings.append(dict(model=model, language=language, runs=len(items), total=n,
                             certified=c, pooled_passver=c/n,
                             mean_run_passver=mean(x['passver'] for x in items),
                             conservative_certified=conservative,
                             conservative_pooled_passver=conservative/n,
                             conservative_mean_run_passver=mean(x['conservative_passver'] for x in items)))
    total = sum(x['total'] for x in runs)
    certified = sum(x['certified'] for x in runs)
    conservative = sum(x['conservative_certified'] for x in runs)
    summary = dict(runs=len(runs), total=total, certified=certified,
                   pooled_passver=certified/total, mean_run_passver=mean(x['passver'] for x in runs),
                   conservative_certified=conservative,
                   conservative_pooled_passver=conservative/total,
                   conservative_mean_run_passver=mean(x['conservative_passver'] for x in runs))
    (OUT / 'passver_reconstruction.json').write_text(json.dumps(dict(summary=summary, settings=settings, runs=runs), indent=2) + '\n')
    lines = ['# PassVer@1 reconstructed from archived RQ1 artifacts', '',
             'Final saved outcomes, including recovery where run. This is not an exact reproduction of Table I.', '',
             'Per run: |proved requirement IDs union passing requirement IDs| / |all requirement IDs|.',
             'Every reconstructed value agrees with its saved summary to the stored rounding precision.', '',
             f"Recorded pooled result: {certified}/{total} = {100*certified/total:.2f}% across {len(runs)} runs.",
             f"Conservative pooled result: {conservative}/{total} = {100*conservative/total:.2f}%.",
             f"Mean of recorded run ratios: {100*summary['mean_run_passver']:.2f}%.", '',
             'Mean/run weights runs equally; pooled weights requirement instances equally. Neither establishes the paper table population or weighting.', '',
             '| Model identifier | Language | Runs | Certified / total | Mean/run (%) | Pooled (%) | Conservative mean/run (%) |',
             '|---|---|---:|---:|---:|---:|---:|']
    for s in settings:
        lines.append(f"| {s['model']} | {s['language']} | {s['runs']} | {s['certified']}/{s['total']} | {100*s['mean_run_passver']:.2f} | {100*s['pooled_passver']:.2f} | {100*s['conservative_mean_run_passver']:.2f} |")
    lines += ['', '## Interpretation limits', '',
              '- These 125 runs cover the ten paper subjects but are not a balanced 180-run matrix; DeepSeek versions are kept separate.',
              '- The conservative view assigns the five final proofs with unresolved axiom status to Uncertified, as requested. It is a changed reporting rule, not the original saved metric.',
              '- The recorded Tested labels include 68 compilation-only requirement instances. These calculations reproduce recorded evidence, not runtime correctness or independently validated SRS satisfaction.',
              '- Baseline exports lack requirement-level passing IDs (the inspected baseline writes an empty list and aggregate test counts). A comparable baseline union cannot be reconstructed from those aggregate counts alone.',
              '- Existing artifact matching and initial-outcome limitations are documented in README.md. No new proof or application execution was performed.', '']
    (OUT / 'passver_reconstruction.md').write_text('\n'.join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
