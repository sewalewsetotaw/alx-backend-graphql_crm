#!/bin/bash
set -euo pipefail

# -------- Paths & Python detection --------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # repo root (where manage.py is)
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Prefer project venv python (Unix or Windows venv layout), fallback to system python
if [ -x "$PROJECT_ROOT/.venv/bin/python" ]; then
  PY="$PROJECT_ROOT/.venv/bin/python"
elif [ -x "$PROJECT_ROOT/venv/bin/python" ]; then
  PY="$PROJECT_ROOT/venv/bin/python"
elif [ -x "$PROJECT_ROOT/.venv/Scripts/python.exe" ]; then
  PY="$PROJECT_ROOT/.venv/Scripts/python.exe"
elif [ -x "$PROJECT_ROOT/venv/Scripts/python.exe" ]; then
  PY="$PROJECT_ROOT/venv/Scripts/python.exe"
elif command -v python3 >/dev/null 2>&1; then
  PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PY="$(command -v python)"
else
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "[$ts] ERROR: python not found" >> "$LOG_FILE"
  exit 1
fi

cd "$PROJECT_ROOT"

# -------- Django-side cleanup logic --------
# Uses Order.order_date (your project has order_date) and Order.customer FK
deleted_count="$("$PY" manage.py shell -c '
from django.utils import timezone
from datetime import timedelta
from django.db.models import Exists, OuterRef
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)

# Subquery: orders for this customer in the last year
recent_orders = Order.objects.filter(customer=OuterRef("pk"), order_date__gte=one_year_ago)

# Customers who DO NOT have recent orders
inactive_qs = Customer.objects.annotate(has_recent=Exists(recent_orders)).filter(has_recent=False)

count = inactive_qs.count()
inactive_qs.delete()
print(count)
')"

# -------- Log result --------
ts="$(date '+%Y-%m-%d %H:%M:%S')"
echo "[$ts] Deleted ${deleted_count:-0} inactive customers" >> "$LOG_FILE"