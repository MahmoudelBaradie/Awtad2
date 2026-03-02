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
