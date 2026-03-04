# Real Estate Development & Property Management ERP (Odoo 19 Community)

This repository delivers a modular custom real estate ERP suite with automated accounting integration.

## Addons
- `real_estate_core`: shared menus, roles, and accounting bridge configuration.
- `real_estate_land`: land acquisition lifecycle with capitalization lock.
- `real_estate_project_wip`: project budgeting, WIP cost accumulation, completion conversion.
- `real_estate_units`: sale/rent unit master.
- `real_estate_sales`: reservation, sales contracts, automated sales/cost journal entries.
- `real_estate_rental`: rental contracts with automated periodic rental posting cron.
- `real_estate_procurement`: contractor contracts with retention and payable posting.
- `real_estate_property`: investment property asset tracking and depreciation basis.
- `real_estate_accounting_bridge`: accounting search/config extension.
- `real_estate_reports`: management reporting menu/actions.
- `real_estate_security`: record-rule extension scaffold.

## Accounting Automation
Every operational module posts accounting entries automatically via configurable accounts from `real.estate.company.config`.

## Installation
1. Copy addons to your Odoo custom addons path.
2. Update app list.
3. Install modules in dependency order beginning with `real_estate_core`.
4. Configure **Real Estate ERP > Configuration > Accounting Bridge**.


## Prerequisites / Troubleshooting
If installation fails with:
`ImportError: Could not load the module 'bs4' to patch`
this is an Odoo server python dependency issue (not specific to these addons).

Install missing dependency in your Odoo virtual environment, then restart Odoo:

```bash
pip install beautifulsoup4
# or
pip install -r requirements.txt
```

For Debian/Ubuntu system Python environments you may also use:

```bash
apt-get install -y python3-bs4
```


## GitHub Merge Conflict Notes
If you see many conflicts across Odoo XML/CSV metadata files in GitHub, this repository uses
`merge=union` via `.gitattributes` to reduce non-overlapping conflicts when merging branches.

If your branch still shows conflicts, update it on your machine and re-push:

```bash
git fetch origin
git checkout <your-branch>
git merge origin/main
# resolve remaining true conflicts, then
git add .
git commit
 git push
```

## حل الكونفلكت خطوة بخطوة (Arabic)
إذا ظهر Conflict في GitHub (خصوصًا في ملفات `*.xml` و `*.csv`) استخدم الخطوات التالية محليًا:

```bash
git fetch origin
git checkout <your-branch>
git pull --rebase origin <your-branch>
git merge origin/main
```

### 1) اعرف الملفات المتعارضة
```bash
git status
```

### 2) حل تعارضات XML/CSV بسرعة (عند كونها إضافات non-overlapping)
> قبل التنفيذ راجع التغييرات للتأكد أنها ليست متضاربة منطقيًا.

```bash
# خذ نسخة الفرع الحالي لكل ملفات XML/CSV المتعارضة
git checkout --ours -- '*.xml' '*.csv'
# أو خذ نسخة main
# git checkout --theirs -- '*.xml' '*.csv'

git add '*.xml' '*.csv'
```

### 3) أكمل الدمج
```bash
git add .
git commit -m "Resolve merge conflicts"
git push
```

### 4) لو كنت تعمل Rebase بدل Merge
```bash
git rebase --continue
# كرر حتى ينتهي
```

### ملاحظات مهمة
- إعداد `.gitattributes` الحالي يساعد على تقليل الكونفلكت لكنه لا يلغي كل التعارضات 100%.
- إذا كان نفس السطر اتعدل في فرعين بشكل مختلف، لازم حل يدوي.
- بعد الحل شغّل فحص سريع:
```bash
python -m compileall real_estate_core real_estate_land real_estate_project_wip real_estate_units real_estate_sales real_estate_rental real_estate_procurement real_estate_property real_estate_accounting_bridge real_estate_reports real_estate_security
```


## Important: Avoid silent XML corruption in merges
If XML files were merged with `merge=union`, Git may create invalid XML (duplicate/misaligned tags)
without conflict markers. This can cause errors like:
`XMLSyntaxError: Opening and ending tag mismatch`.

Use default merge behavior for XML (current `.gitattributes`), then validate before push:

```bash
python - <<'PY2'
from pathlib import Path
from lxml import etree
for f in Path('.').rglob('*.xml'):
    if 'real_estate_' in str(f):
        etree.parse(str(f))
print('all real_estate xml files are valid')
PY2
```


## Quick XML sanity check before Odoo upgrade
Run this before installing/upgrading modules on the server to catch malformed XML early:

```bash
python scripts/validate_real_estate_xml.py
```


## Fix for: No matching record found for external id `real_estate_security.group_*`
If your server still shows this error during install/upgrade, it usually means your deployed branch still has old
references or mixed commits.

This repository now includes compatibility aliases for `real_estate_security.group_*` -> `real_estate_core.group_*`.
After pulling latest commits:

```bash
python scripts/validate_real_estate_xml.py
# restart odoo service
# then upgrade modules from Apps (or -u real_estate_core,real_estate_units)
```


## Check deployment mismatch (legacy group xmlids)
If your server still throws errors containing:
`real_estate_security.group_real_estate_*`
it means deployed files are older/mixed.

Run before restart:

```bash
python scripts/check_legacy_group_xmlids.py
```

If script fails, pull latest branch and make sure these access files reference
`real_estate_core.group_*` only.
