from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import List, Optional
from .common import OrmBase


class SalesAgreementItemBase(OrmBase):
    product_id: int
    quantity: Decimal
    price: Decimal

class SalesAgreementItemCreate(SalesAgreementItemBase):
    pass

class SalesAgreementItem(SalesAgreementItemBase):
    id: int


class SalesAgreementBase(OrmBase):
    organization_id: int
    customer_id: int
    agreement_number: Optional[str] = None
    agreement_date: date
    city: str
    seller_representative: str
    seller_basis: str
    subject_description: Optional[str] = None

    buyer_passport_series: Optional[str] = None
    buyer_passport_number: Optional[str] = None
    buyer_passport_issued_by: Optional[str] = None
    buyer_passport_issued_at: Optional[date] = None
    buyer_address: Optional[str] = None

    buyer_bank_account: Optional[str] = None
    buyer_bank_name: Optional[str] = None
    buyer_bank_corr_account: Optional[str] = None
    buyer_bank_bik: Optional[str] = None

    dispute_resolution: Optional[str] = None
    vat_rate: Optional[Decimal] = None

class SalesAgreementCreate(SalesAgreementBase):
    items: List[SalesAgreementItemCreate] = []

class SalesAgreementUpdate(SalesAgreementBase):
    items: List[SalesAgreementItemCreate] = []

class SalesAgreement(SalesAgreementBase):
    id: int
    items: List[SalesAgreementItem] = []
