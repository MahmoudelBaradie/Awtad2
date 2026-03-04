from pathlib import Path
import sys
import xml.etree.ElementTree as ET

errors = []
for path in sorted(Path('.').rglob('*.xml')):
    p = str(path)
    if 'real_estate_' not in p:
        continue
    try:
        ET.parse(p)
    except Exception as exc:
        errors.append((p, exc))

if errors:
    for p, exc in errors:
        print(f"ERROR: {p}: {exc}")
    sys.exit(1)

print('All real_estate XML files are well-formed.')
