from pathlib import Path
import sys

bad = []
for path in sorted(Path('.').rglob('ir.model.access.csv')):
    text = path.read_text(encoding='utf-8')
    if 'real_estate_security.group_real_estate_' in text:
        bad.append(path)

if bad:
    print('Found legacy group xmlid references (real_estate_security.group_*) in:')
    for p in bad:
        print(f' - {p}')
    print('Please replace with real_estate_core.group_* or pull latest branch.')
    sys.exit(1)

print('No legacy group xmlid references were found in access CSV files.')
