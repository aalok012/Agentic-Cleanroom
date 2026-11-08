"""Read-only reconciliation of paper Table I, workbook cells and raw exports."""
import csv
import json
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/reviewer_audit'
NS = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
MODEL = {
    'anthropic_claude-sonnet-4-6': 'Sonnet',
    'anthropic_claude-haiku-4_5': 'Haiku',
    'openai_gpt-5_1': 'GPT-5.1',
    'google_gemini-3_1-pro-preview': 'Gemini Pro',
    'google_gemini-3-flash-preview': 'Gemini Flash',
    'deepseek_deepseek-v3_2': 'DeepSeek',
    'deepseek_deepseek-v3_2-20251201': 'DeepSeek',
}
# Transcribed from PDF Table I; Java/Python/JS/Avg VPR, then same order TPR.
PAPER = {
 ('Sonnet','Baseline'): '58.55 52.93 48.21 53.23 83.33 43.61 42.54 56.49',
 ('Sonnet','Pipeline'): '65.09 87.88 91.21 81.39 20.00 28.18 28.00 25.39',
 ('Haiku','Baseline'): '32.85 35.86 32.85 33.85 97.73 50.60 38.66 62.33',
 ('Haiku','Pipeline'): '43.16 66.52 45.25 51.64 0.00 0.00 61.23 20.41',
 ('GPT-5.1','Baseline'): '51.44 37.46 29.80 39.57 98.75 25.58 20.61 48.32',
 ('GPT-5.1','Pipeline'): '35.37 66.94 53.82 52.04 50.00 9.10 64.48 41.19',
 ('Gemini Pro','Baseline'): '76.73 54.79 88.73 73.42 66.67 48.45 32.55 49.22',
 ('Gemini Pro','Pipeline'): '100.00 96.67 100.00 98.81 0.00 0.00 0.00 0.00',
 ('Gemini Flash','Baseline'): '17.21 16.50 16.50 16.74 95.00 45.38 36.50 58.96',
 ('Gemini Flash','Pipeline'): '72.53 100.00 75.75 82.76 0.00 0.00 77.08 25.69',
 ('DeepSeek','Baseline'): '19.25 15.91 23.29 19.48 91.90 36.78 33.00 53.89',
 ('DeepSeek','Pipeline'): '49.54 80.66 45.23 58.48 0.00 16.36 57.76 24.71',
 ('Average','Baseline'): '42.97 34.73 38.75 38.82 89.44 39.00 32.18 53.54',
 ('Average','Pipeline'): '56.19 81.42 64.53 67.48 14.29 10.48 49.63 24.90',
}


def mean(xs):
    return sum(xs) / len(xs)


def fmt(value):
    return str(value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))


def main():
    with zipfile.ZipFile(ROOT / 'results/organized_results.xlsx') as z:
        strings = [''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('x:si', NS)]
        rows = []
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//x:sheetData/x:row', NS):
            d = {'row': row.get('r')}
            for cell in row:
                v = cell.find('x:v', NS)
                if v is None:
                    continue
                # Worksheet numbers are stored with binary serialization tails. Restore
                # the four-decimal precision of the source CSVs before decimal averaging.
                value = strings[int(v.text)] if cell.get('t') == 's' else Decimal(v.text).quantize(Decimal('.0001'))
                d[''.join(filter(str.isalpha, cell.get('r')))] = value
            if d.get('B') in ('Pipeline', 'Baseline'):
                rows.append(d)
    raw = defaultdict(list)
    for name, arm in [('experiment_metrics.csv','Pipeline'), ('baseline_metrics.csv','Baseline'),
                      ('baseline_runpy_newmodels_metrics.csv','Baseline')]:
        with (ROOT / 'results/raw_results' / name).open() as f:
            for line, r in enumerate(csv.DictReader(f), 2):
                if r['status'] == 'complete':
                    raw[arm, r['model'], r['srs'], r['language']].append(dict(r, source=name, csv_line=line))
    members = {}
    for r in rows:
        for language, vc, tc in [('java','F','I'), ('python','G','J'), ('javascript','H','K')]:
            if not isinstance(r.get(vc), Decimal):
                continue
            key = (r['B'], r['A'], r['C'], language)
            matches = [x for x in raw[key] if Decimal(x['verification_pass_ratio']) == r[vc]
                       and Decimal(x['test_case_pass_ratio']) == r[tc]]
            assert matches, ('No raw match', r['row'], key)
            match = max(matches, key=lambda x:x['timestamp'])
            members[key] = dict(match, workbook_row=r['row'], workbook_cells=f'{vc}{r["row"]}/{tc}{r["row"]}')
    comparison = []
    for (model, arm), numbers in PAPER.items():
        selected = [r for r in rows if r['B'] == arm and (model == 'Average' or MODEL[r['A']] == model)]
        actual = []
        for cols in ['FGH', 'IJK']:
            actual += [mean([r[c] for r in selected if isinstance(r.get(c), Decimal)])*100 for c in cols]
            actual += [mean([r[c] for r in selected for c in cols if isinstance(r.get(c), Decimal)])*100]
        expected = numbers.split()
        reconstructed = list(map(fmt, actual))
        assert all(abs(a - Decimal(e)) <= Decimal('0.00500001') for a,e in zip(actual,expected)), (model, arm, expected, reconstructed)
        comparison.append(dict(model=model, approach=arm, paper=expected, workbook=reconstructed, half_up_rounding_differences=sum(a != b for a,b in zip(expected,reconstructed))))
    subjects = {p.stem for p in (ROOT / 'data/srs').glob('*.xml')}
    all_available = {k: max(v,key=lambda r:r['timestamp']) for k,v in raw.items()
                     if k[1] in MODEL and k[2] in subjects}
    extras = [dict(r, approach=k[0])
              for k,r in all_available.items() if k not in members]
    expanded = []
    for model, arm in PAPER:
        selected = [r for k,r in all_available.items() if k[0] == arm and (model == 'Average' or MODEL[k[1]] == model)]
        expanded.append(dict(model=model, approach=arm, runs=len(selected),
                             vpr=fmt(mean([Decimal(r['verification_pass_ratio'])*100 for r in selected])),
                             tpr=fmt(mean([Decimal(r['test_case_pass_ratio'])*100 for r in selected]))))
    # Characterize matched availability without assuming the two versions are identical.
    arms = {arm: {k[1:] for k in members if k[0] == arm} for arm in ['Pipeline','Baseline']}
    shared = arms['Pipeline'] & arms['Baseline']
    summary = dict(paper_cells_checked=112, paper_cells_matching_within_rounding=112,
                   half_up_rounding_differences=sum(x['half_up_rounding_differences'] for x in comparison),
                   workbook_pipeline_runs=len(arms['Pipeline']), workbook_baseline_runs=len(arms['Baseline']),
                   matched_exact_model_subject_language_cells=len(shared),
                   extra_raw_pipeline_runs=sum(x['approach']=='Pipeline' for x in extras))
    output = dict(summary=summary, paper_comparison=comparison, all_available_means=expanded,
                  omitted_from_workbook=extras, workbook_run_manifest=list(members.values()))
    (OUT / 'rq1_table_reconciliation.json').write_text(json.dumps(output,indent=2)+'\n')
    lines = ['# RQ1 Table I reconciliation', '',
             'The paper table matches the selected workbook data. It does not aggregate all completed pipeline runs in the raw exports.', '',
             '- All 112 paper VPR/TPR values (including row/column averages) agree within rounding tolerance (0.005 percentage points); exact half-way rounding can differ by 0.01 in displayed values.',
             '- All 107 pipeline and 120 baseline workbook run entries match a completed raw-export entry on model, subject, language, VPR and TPR.',
             '- The raw exports contain 18 further completed pipeline runs for the ten paper subjects and six model families. They are omitted from the workbook.',
             '- Numerical reconciliation does not independently validate original requirement satisfaction, labels, or experimental fairness.', '',
             '| Model | Approach | Paper VPR avg (%) | All available VPR avg (%) | Paper TPR avg (%) | All available TPR avg (%) | Available runs |',
             '|---|---|---:|---:|---:|---:|---:|']
    for x in expanded:
        p=PAPER[x['model'],x['approach']].split()
        lines.append(f"| {x['model']} | {x['approach']} | {p[3]} | {x['vpr']} | {p[7]} | {x['tpr']} | {x['runs']} |")
    lines += ['', '## How the published averages are formed', '',
              'Average the available numeric workbook cells, ignoring the missing Gemini Pro Java/DineOut cell. Overall averages weight each included run equally, not each model family equally. DeepSeek-V3.2 and DeepSeek-V3.2-20251201 are combined in one paper row. Calculations use four-decimal input ratios. Some published values use a different half-way rounding result than decimal half-up; these 0.01 display differences are not substantive data mismatches.', '',
              'Workbook pipeline coverage: Sonnet 15 runs (5 subjects), Haiku 12 (4), GPT-5.1 24 (8), Gemini Pro 14 (5 subjects with one missing language), Gemini Flash 12 (4), DeepSeek 30 (10 version/subject entries but only 9 distinct subjects; FoodSaver appears for both versions). KinMail is absent from the entire pipeline worksheet section.', '',
              'Workbook baseline coverage: Sonnet 18, Haiku 12, GPT-5.1 30, Gemini Pro 18, Gemini Flash 12, DeepSeek 30. Only 104 exact model-version/subject/language cells are shared by the selected pipeline and baseline arms. Thus this is not a complete or fully paired 6 x 10 x 3 comparison.', '',
              '## Completed pipeline runs omitted from workbook', '',
              '| Model | Subject | Languages |', '|---|---|---|']
    extra_groups=defaultdict(list)
    for x in extras:
        extra_groups[x['model'],x['srs']].append(x['language'])
    for (model,srs),langs in sorted(extra_groups.items()):
        lines.append(f"| {model} | {srs} | {', '.join(sorted(langs))} |")
    lines += ['', '## Consequences', '',
              '- Published headline baseline VPR 38.82% and pipeline VPR 67.48% are reproducible for the workbook selection. Including the additional archived pipeline runs gives 64.92% pipeline VPR and 28.91% pipeline TPR; baseline remains 38.82% and 53.54%. These expanded means are descriptive, not a recommended replacement paired analysis.',
              '- The earlier 125-run PassVer@1/label reconstruction uses a different population from the 107-run pipeline table. Do not combine those results as if their populations were identical.',
              '- The paper statement of improvement for all model-language settings is contradicted by GPT-5.1 Java (35.37% pipeline versus 51.44% baseline) in its own table.',
              '- Before revision, explicitly choose a common run manifest, document excluded/failed/missing runs and model versions, and recompute VPR, TPR and PassVer@1 consistently from that manifest.',
              '- Sources read: paper Table I (PDF page 7), organized_results.xlsx sheet "RQ1-effectiveness ", experiment_metrics.csv, baseline_metrics.csv and baseline_runpy_newmodels_metrics.csv. Original sources were not edited.', '']
    (OUT / 'rq1_table_reconciliation.md').write_text('\n'.join(lines))
    print(json.dumps(summary,indent=2))
    print('All available means:', expanded[-2:])


if __name__ == '__main__':
    main()
