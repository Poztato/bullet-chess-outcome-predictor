"""Verify recovered artifacts without importing or executing project code."""

import argparse
import ast
import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def verify(include_local_backups=False):
    manifest = json.loads((ROOT / 'docs/recovery-manifest.json').read_text(encoding='utf-8'))
    failures = []
    checked = set()
    skipped = 0
    maintained_docs = [
        'README.md', 'AGENTS.md', 'CHANGELOG.md', 'archive/README.md',
        'archive/extension-prototypes/README.md', 'archive/reference-extensions/README.md',
        'models/README.md', 'data/README.md', 'extension/README.md',
        'docs/recovery-audit.md', 'docs/phase-2-plan.md',
    ]
    for destination in maintained_docs:
        path = ROOT / destination
        if not path.is_file():
            failures.append(f'Missing project documentation: {destination}')
            continue
        content = path.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if target.startswith(('https://', 'http://', '#')):
                continue
            target_path = target.split('#', 1)[0]
            if not (path.parent / target_path).exists():
                failures.append(f'Broken local link in {destination}: {target}')
        if '\u2014' in content:
            failures.append(f'Em dash in maintained documentation: {destination}')
    for entry in manifest['entries']:
        if not entry['tracked'] and not include_local_backups:
            skipped += 1
            continue
        destination = entry['destination']
        path = (ROOT / destination).resolve()
        if not path.is_relative_to(ROOT):
            failures.append(f'Path outside repository: {destination}')
            continue
        if not path.is_file():
            failures.append(f'Missing preserved file: {destination}')
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry['sha256']:
            failures.append(f'Hash mismatch: {destination} (source: {entry["source"]})')
        checked.add(destination)

    dataset = ROOT / 'data/processed/final_dataset.csv'
    with dataset.open(encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        expected = ['game_id', 'is_white', 'avg_pr', 'sesh_cnt', 'elo_diff', 'streak', 'result']
        if reader.fieldnames != expected:
            failures.append('Unexpected final dataset column order')
        else:
            if len(rows) != 8542 or len({r['game_id'] for r in rows}) != 8542:
                failures.append('Final dataset row count or unique IDs changed')
            if Counter(r['result'] for r in rows) != {'1.0': 4189, '0.0': 4074, '0.5': 279}:
                failures.append('Final dataset class counts changed')
            for index, row in enumerate(rows, start=2):
                try:
                    valid = all(math.isfinite(float(row[key])) for key in expected[1:])
                except (TypeError, ValueError):
                    valid = False
                if not valid:
                    failures.append(f'Invalid numeric dataset value at CSV line {index}')
                    break

    parsed = 0
    for folder in ['scripts', 'archive', 'notebooks']:
        for path in sorted((ROOT / folder).rglob('*')):
            if path.suffix == '.py':
                try:
                    ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
                    parsed += 1
                except (SyntaxError, UnicodeError) as error:
                    failures.append(f'Invalid Python: {path.relative_to(ROOT)}: {error}')
            elif path.suffix == '.ipynb':
                try:
                    notebook = json.loads(path.read_text(encoding='utf-8'))
                    if notebook['nbformat'] != 4:
                        raise ValueError('Expected notebook format 4')
                    for index, cell in enumerate(notebook['cells']):
                        if cell['cell_type'] == 'code':
                            ast.parse(''.join(cell['source']), filename=f'{path}:cell-{index}')
                    parsed += 1
                except (KeyError, ValueError, SyntaxError) as error:
                    failures.append(f'Invalid notebook: {path.relative_to(ROOT)}: {error}')

    metadata = json.loads((ROOT / 'models/baseline-metadata.json').read_text(encoding='utf-8'))
    model_path = ROOT / metadata['artifact']
    if hashlib.sha256(model_path.read_bytes()).hexdigest() != metadata['sha256']:
        failures.append('Model metadata hash does not match the preserved artifact')
    if metadata['feature_names'] != expected[1:-1] or metadata['classes'] != ['Draw', 'Lose', 'Win']:
        failures.append('Unexpected baseline feature or class contract')

    if failures:
        for failure in failures:
            print('FAIL:', failure)
        return 1
    print(f'PASS: {len(checked)} preserved files verified; {parsed} Python/notebook files parsed.')
    print('PASS: 8,542 unique games, dataset values/class counts, and baseline metadata verified.')
    if skipped:
        print(f'INFO: {skipped} local-only source entries skipped, expected on a fresh clone.')
    print('No archived scripts, training, network requests, or engine processes executed.')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-local-backups', action='store_true',
                        help='Also check original local-only files on the recovery machine.')
    arguments = parser.parse_args()
    raise SystemExit(verify(arguments.include_local_backups))
