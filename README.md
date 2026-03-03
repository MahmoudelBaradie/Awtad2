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

 codex/develop-real-estate-erp-system-in-odoo-6i28zi

 codex/develop-real-estate-erp-system-in-odoo-s9ejpp
 main



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

 codex/develop-real-estate-erp-system-in-odoo-6i28zi



