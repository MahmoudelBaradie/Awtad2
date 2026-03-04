#!/usr/bin/env bash
set -euo pipefail

# Stable conflict resolver for this repository.
# It keeps the current branch version (--ours) for known high-churn files,
# then validates XML and legacy group xmlids.

FILES=(
  ".gitattributes"
  "README.md"
  "real_estate_accounting_bridge/views/real_estate_accounting_bridge_views.xml"
  "real_estate_core/__manifest__.py"
  "real_estate_core/data/sequence_data.xml"
  "real_estate_core/models/__init__.py"
  "real_estate_core/security/ir.model.access.csv"
  "real_estate_core/security/real_estate_core_security.xml"
  "real_estate_core/views/real_estate_config_views.xml"
  "real_estate_core/views/real_estate_menu.xml"
  "real_estate_land/models/real_estate_land.py"
  "real_estate_land/security/ir.model.access.csv"
  "real_estate_land/views/real_estate_land_views.xml"
  "real_estate_procurement/models/real_estate_procurement.py"
  "real_estate_procurement/security/ir.model.access.csv"
  "real_estate_procurement/views/real_estate_procurement_views.xml"
  "real_estate_project_wip/models/real_estate_project.py"
  "real_estate_project_wip/security/ir.model.access.csv"
  "real_estate_project_wip/views/real_estate_project_views.xml"
  "real_estate_property/security/ir.model.access.csv"
  "real_estate_property/views/real_estate_property_views.xml"
  "real_estate_rental/data/cron_data.xml"
  "real_estate_rental/models/real_estate_rental.py"
  "real_estate_rental/security/ir.model.access.csv"
  "real_estate_rental/views/real_estate_rental_views.xml"
)

echo "Resolving known files using --ours..."
for f in "${FILES[@]}"; do
  if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
    git checkout --ours -- "$f" 2>/dev/null || true
    git add "$f" || true
  fi
done

echo "Checking for unresolved conflict markers..."
if rg -n "^(<<<<<<<|=======|>>>>>>>)" "${FILES[@]}"; then
  echo "Conflict markers still exist. Resolve manually, then re-run." >&2
  exit 1
fi

echo "Running validation..."
python scripts/validate_real_estate_xml.py
python scripts/check_legacy_group_xmlids.py

echo "Done. If merge is complete, run:"
echo "  git commit -m 'Resolve merge conflicts (stable mode)'"
