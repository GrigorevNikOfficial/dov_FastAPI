# app/templating.py
from __future__ import annotations

from datetime import datetime, date, timezone
from decimal import Decimal, ROUND_HALF_UP
from fastapi.templating import Jinja2Templates

_templates: Jinja2Templates | None = None

def _rusdate(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%d.%m.%Y")
    try:
        # если пришла строка 'YYYY-MM-DD'
        return datetime.fromisoformat(str(value)).strftime("%d.%m.%Y")
    except Exception:
        return value


def _money(value):
    if value is None:
        return "0.00"
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except Exception:
            return str(value)
    quantized = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{quantized}"

def get_templates() -> Jinja2Templates:
    global _templates
    if _templates is None:
        t = Jinja2Templates(directory="app/templates")
        t.env.globals["now"] = lambda: datetime.now(timezone.utc)
        t.env.filters["rusdate"] = _rusdate
        t.env.filters["money"] = _money
        _templates = t
    return _templates