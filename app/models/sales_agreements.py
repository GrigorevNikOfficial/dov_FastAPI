from __future__ import annotations
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from ..database import Base


class SalesAgreement(Base):
    __tablename__ = "sales_agreements"

    id = Column(Integer, primary_key=True, index=True)
    agreement_number = Column(String(50), nullable=True)
    agreement_date = Column(Date, nullable=False)
    city = Column(String(100), nullable=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    seller_representative = Column(String(255), nullable=False)
    seller_basis = Column(String(255), nullable=False)
    subject_description = Column(Text, nullable=True)

    buyer_passport_series = Column(String(50), nullable=True)
    buyer_passport_number = Column(String(50), nullable=True)
    buyer_passport_issued_by = Column(String(255), nullable=True)
    buyer_passport_issued_at = Column(Date, nullable=True)
    buyer_address = Column(String(255), nullable=True)

    buyer_bank_account = Column(String(100), nullable=True)
    buyer_bank_name = Column(String(255), nullable=True)
    buyer_bank_corr_account = Column(String(100), nullable=True)
    buyer_bank_bik = Column(String(50), nullable=True)

    dispute_resolution = Column(String(255), nullable=True)
    vat_rate = Column(Numeric(5, 2), nullable=True)

    organization = relationship("Organization")
    customer = relationship("Customer")

    items = relationship(
        "SalesAgreementItem",
        back_populates="agreement",
        cascade="all, delete-orphan",
    )


class SalesAgreementItem(Base):
    __tablename__ = "sales_agreement_items"

    id = Column(Integer, primary_key=True, index=True)
    agreement_id = Column(Integer, ForeignKey("sales_agreements.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    agreement = relationship("SalesAgreement", back_populates="items")
    product = relationship("Product")
