from __future__ import annotations
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..templating import get_templates
from ..crud import sales_agreement as crud_agreement
from ..crud import organization as crud_org
from ..crud import customer as crud_customer
from ..crud import product as crud_product
from ..crud import unit as crud_unit
from ..schemas.sales_agreements import (
    SalesAgreementCreate,
    SalesAgreementUpdate,
    SalesAgreementItemCreate,
)


templates = get_templates()
router = APIRouter()


def _optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _optional_decimal(value: Optional[str]) -> Optional[Decimal]:
    raw = _optional(value)
    if raw is None:
        return None
    try:
        return Decimal(raw)
    except Exception:
        return None


def _build_items(
    product_ids: List[int],
    unit_ids: List[int],
    quantities: List[str],
    prices: List[str],
) -> List[SalesAgreementItemCreate]:
    items: List[SalesAgreementItemCreate] = []
    for pid, uid, qty, price in zip(product_ids, unit_ids, quantities, prices):
        qty_val = _optional_decimal(qty)
        price_val = _optional_decimal(price)
        if pid is None or uid is None or qty_val is None or price_val is None:
            continue
        items.append(
            SalesAgreementItemCreate(
                product_id=int(pid),
                unit_id=int(uid),
                quantity=qty_val,
                price=price_val,
            )
        )
    return items


@router.get("/", response_class=HTMLResponse)
def list_agreements(request: Request, db: Session = Depends(get_db)):
    agreements = crud_agreement.get_sales_agreements(db)
    return templates.TemplateResponse(
        "sales_agreements/list.html",
        {"request": request, "agreements": agreements},
    )


@router.get("/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    orgs = crud_org.get_organizations(db)
    customers = crud_customer.get_customers(db)
    products = crud_product.get_products(db)
    units = crud_unit.get_units(db)
    return templates.TemplateResponse(
        "sales_agreements/create.html",
        {
            "request": request,
            "orgs": orgs,
            "customers": customers,
            "products": products,
            "units": units,
        },
    )


@router.post("/create")
def create_agreement(
    organization_id: int = Form(...),
    customer_id: int = Form(...),
    agreement_number: Optional[str] = Form(None),
    agreement_date: str = Form(...),
    city: str = Form(...),
    seller_representative: str = Form(...),
    seller_basis: str = Form(...),
    subject_description: Optional[str] = Form(None),
    buyer_passport_series: Optional[str] = Form(None),
    buyer_passport_number: Optional[str] = Form(None),
    buyer_passport_issued_by: Optional[str] = Form(None),
    buyer_passport_issued_at: Optional[str] = Form(None),
    buyer_address: Optional[str] = Form(None),
    buyer_bank_account: Optional[str] = Form(None),
    buyer_bank_name: Optional[str] = Form(None),
    buyer_bank_corr_account: Optional[str] = Form(None),
    buyer_bank_bik: Optional[str] = Form(None),
    dispute_resolution: Optional[str] = Form(None),
    vat_rate: Optional[str] = Form(None),
    product_id: List[int] = Form([]),
    unit_id: List[int] = Form([]),
    quantity: List[str] = Form([]),
    price: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    items = _build_items(product_id, unit_id, quantity, price)
    obj_in = SalesAgreementCreate(
        organization_id=organization_id,
        customer_id=customer_id,
        agreement_number=_optional(agreement_number),
        agreement_date=agreement_date,
        city=city,
        seller_representative=seller_representative,
        seller_basis=seller_basis,
        subject_description=_optional(subject_description),
        buyer_passport_series=_optional(buyer_passport_series),
        buyer_passport_number=_optional(buyer_passport_number),
        buyer_passport_issued_by=_optional(buyer_passport_issued_by),
        buyer_passport_issued_at=_optional(buyer_passport_issued_at),
        buyer_address=_optional(buyer_address),
        buyer_bank_account=_optional(buyer_bank_account),
        buyer_bank_name=_optional(buyer_bank_name),
        buyer_bank_corr_account=_optional(buyer_bank_corr_account),
        buyer_bank_bik=_optional(buyer_bank_bik),
        dispute_resolution=_optional(dispute_resolution),
        vat_rate=_optional_decimal(vat_rate),
        items=items,
    )
    crud_agreement.create_sales_agreement(db, obj_in)
    return RedirectResponse(url="/sales-agreements", status_code=303)


@router.get("/{agreement_id}/edit", response_class=HTMLResponse)
def edit_form(agreement_id: int, request: Request, db: Session = Depends(get_db)):
    agreement = crud_agreement.get_sales_agreement(db, agreement_id)
    orgs = crud_org.get_organizations(db)
    customers = crud_customer.get_customers(db)
    products = crud_product.get_products(db)
    units = crud_unit.get_units(db)
    return templates.TemplateResponse(
        "sales_agreements/edit.html",
        {
            "request": request,
            "agreement": agreement,
            "orgs": orgs,
            "customers": customers,
            "products": products,
            "units": units,
        },
    )


@router.post("/{agreement_id}/edit")
def update_agreement(
    agreement_id: int,
    organization_id: int = Form(...),
    customer_id: int = Form(...),
    agreement_number: Optional[str] = Form(None),
    agreement_date: str = Form(...),
    city: str = Form(...),
    seller_representative: str = Form(...),
    seller_basis: str = Form(...),
    subject_description: Optional[str] = Form(None),
    buyer_passport_series: Optional[str] = Form(None),
    buyer_passport_number: Optional[str] = Form(None),
    buyer_passport_issued_by: Optional[str] = Form(None),
    buyer_passport_issued_at: Optional[str] = Form(None),
    buyer_address: Optional[str] = Form(None),
    buyer_bank_account: Optional[str] = Form(None),
    buyer_bank_name: Optional[str] = Form(None),
    buyer_bank_corr_account: Optional[str] = Form(None),
    buyer_bank_bik: Optional[str] = Form(None),
    dispute_resolution: Optional[str] = Form(None),
    vat_rate: Optional[str] = Form(None),
    product_id: List[int] = Form([]),
    unit_id: List[int] = Form([]),
    quantity: List[str] = Form([]),
    price: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    items = _build_items(product_id, unit_id, quantity, price)
    obj_in = SalesAgreementUpdate(
        organization_id=organization_id,
        customer_id=customer_id,
        agreement_number=_optional(agreement_number),
        agreement_date=agreement_date,
        city=city,
        seller_representative=seller_representative,
        seller_basis=seller_basis,
        subject_description=_optional(subject_description),
        buyer_passport_series=_optional(buyer_passport_series),
        buyer_passport_number=_optional(buyer_passport_number),
        buyer_passport_issued_by=_optional(buyer_passport_issued_by),
        buyer_passport_issued_at=_optional(buyer_passport_issued_at),
        buyer_address=_optional(buyer_address),
        buyer_bank_account=_optional(buyer_bank_account),
        buyer_bank_name=_optional(buyer_bank_name),
        buyer_bank_corr_account=_optional(buyer_bank_corr_account),
        buyer_bank_bik=_optional(buyer_bank_bik),
        dispute_resolution=_optional(dispute_resolution),
        vat_rate=_optional_decimal(vat_rate),
        items=items,
    )
    db_obj = crud_agreement.get_sales_agreement(db, agreement_id)
    crud_agreement.update_sales_agreement(db, db_obj, obj_in)
    return RedirectResponse(url="/sales-agreements", status_code=303)


@router.get("/{agreement_id}/print", response_class=HTMLResponse)
def print_view(agreement_id: int, request: Request, db: Session = Depends(get_db)):
    agreement = crud_agreement.get_sales_agreement(db, agreement_id)
    return templates.TemplateResponse(
        "sales_agreements/print.html",
        {"request": request, "agreement": agreement},
    )


@router.get("/{agreement_id}/delete", response_class=HTMLResponse)
def delete_form(agreement_id: int, request: Request, db: Session = Depends(get_db)):
    agreement = crud_agreement.get_sales_agreement(db, agreement_id)
    return templates.TemplateResponse(
        "sales_agreements/delete.html",
        {"request": request, "agreement": agreement},
    )


@router.post("/{agreement_id}/delete")
def delete_agreement(agreement_id: int, db: Session = Depends(get_db)):
    db_obj = crud_agreement.get_sales_agreement(db, agreement_id)
    crud_agreement.delete_sales_agreement(db, db_obj)
    return RedirectResponse(url="/sales-agreements", status_code=303)
