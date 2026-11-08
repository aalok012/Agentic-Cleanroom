"""PassVer@1 for the exact pipeline run selection reconstructed from Table I."""
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/reviewer_audit'
NAMES = {
    'anthropic_claude-sonnet-4-6': 'Claude Sonnet 4.6',
    'anthropic_claude-haiku-4_5': 'Claude Haiku 4.5',
    'openai_gpt-5_1': 'GPT-5.1',
    'google_gemini-3_1-pro-preview': 'Gemini 3.1 Pro',
    'google_gemini-3-flash-preview': 'Gemini 3 Flash',
    'deepseek_deepseek-v3_2': 'DeepSeek-V3.2',
    'deepseek_deepseek-v3_2-20251201': 'DeepSeek-V3.2',
}


def main():
    table = json.loads((OUT / 'rq1_table_reconciliation.json').read_text())
    archive = json.loads((OUT / 'passver_reconstruction.json').read_text())
    lookup = {r['run_id']: r for r in archive['runs']}
    selected = [r for r in table['workbook_run_manifest'] if r['source'] == 'experiment_metrics.csv']
    assert len(selected) == 107
    groups = defaultdict(list)
    runs = []
    for row in selected:
        r = lookup[row['run_id']]
        assert (r['model'], r['srs'], r['language']) == (row['model'], row['srs'], row['language'])
        assert abs(r['passver'] - float(row['PassVer@1'])) < .00011
        groups[NAMES[r['model']]].append(r)
        runs.append(r)
    assert len({r['run_id'] for r in runs}) == 107
    order = list(dict.fromkeys(NAMES.values()))
    rows = []
    for name in order + ['Overall']:
        items = runs if name == 'Overall' else groups[name]
        rec = {'model': name, 'runs': len(items)}
        for label, metric in [('recorded','passver'), ('conservative','conservative_passver')]:
            for lang in ['java','python','javascript']:
                subset = [r for r in items if r['language'] == lang]
                rec[lang + '_runs'] = len(subset)
                rec[label + '_' + lang] = mean(r[metric] for r in subset) * 100
            rec[label + '_average'] = mean(r[metric] for r in items) * 100
        rows.append(rec)
    (OUT / 'table1_passver.json').write_text(json.dumps({'rows': rows, 'runs': runs},indent=2)+'\n')
    lines = ['# PassVer@1 for the Table I pipeline population', '',
             'Exact selection: 107 pipeline runs matched from the RQ1-effectiveness workbook. These are saved final outcomes, including recovery where it ran. Original recorded proof/test rules are used in the primary table, consistent with Table I VPR.', '',
             'For each run, calculate the union of proved requirement IDs and test-passing requirement IDs, divided by all requirement IDs. Language cells average the selected run ratios; the Avg column averages all selected run ratios for that model. Overall weights runs equally, as Table I does. Calculations use unrounded reconstructed ratios; saved four-decimal summaries agree within their rounding precision.', '',
             '| Model | Java (%) | Python (%) | JavaScript (%) | Avg (%) | Runs (Java/Python/JS) |',
             '|---|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['model']} | {r['recorded_java']:.2f} | {r['recorded_python']:.2f} | {r['recorded_javascript']:.2f} | {r['recorded_average']:.2f} | {r['java_runs']}/{r['python_runs']}/{r['javascript_runs']} |")
    lines += ['', '## Alternative conservative label policy', '',
              'Moving the five final proved instances with unresolved axiom status to Uncertified changes DeepSeek Python to 86.45%, DeepSeek Avg to 64.29%, Overall Python to '
              f"{rows[-1]['conservative_python']:.2f}%, and Overall Avg to {rows[-1]['conservative_average']:.2f}%. Other cells are unchanged. This policy differs from Table I VPR and should not be silently mixed with its original labels.", '',
              '## Scope', '',
              '- DeepSeek versions are combined to reproduce Table I grouping. Unequal subject coverage is retained exactly, not repaired by adding runs.',
              '- These are pipeline values. A corresponding baseline PassVer@1 cannot be obtained from the available aggregate test counts alone because requirement-level passing IDs are missing.',
              '- Java/Spring recorded test passes are compilation checks. The numbers report recorded certification, not independent validation of SRS satisfaction.',
              '- The overall 76.13% is a mean of run ratios. Pooling requirements yields a different quantity and is not the table averaging method.',
              '- See rq1_table_reconciliation.md for the exact population and exclusions. No source files or original result artifacts were changed.', '']
    (OUT / 'table1_passver.md').write_text('\n'.join(lines))
    print('\n'.join(lines[:15]))


if __name__ == '__main__':
    main()
