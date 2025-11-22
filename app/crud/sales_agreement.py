from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import sales_agreements as schemas


def get_sales_agreement(db: Session, id: int):
    return db.query(models.SalesAgreement).get(id)


def get_sales_agreements(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.SalesAgreement)
        .order_by(models.SalesAgreement.agreement_date.desc(), models.SalesAgreement.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_sales_agreement(db: Session, obj_in: schemas.SalesAgreementCreate):
    header_data = obj_in.model_dump(exclude={"items"})
    agreement = models.SalesAgreement(**header_data)
    db.add(agreement)
    db.flush()

    for item in obj_in.items:
        db.add(
            models.SalesAgreementItem(
                agreement_id=agreement.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
        )

    db.commit()
    db.refresh(agreement)
    return agreement


def update_sales_agreement(
    db: Session,
    db_obj: models.SalesAgreement,
    obj_in: schemas.SalesAgreementUpdate,
):
    header_data = obj_in.model_dump(exclude={"items"})
    for key, value in header_data.items():
        setattr(db_obj, key, value)

    db.query(models.SalesAgreementItem).filter(
        models.SalesAgreementItem.agreement_id == db_obj.id
    ).delete()
    db.flush()

    for item in obj_in.items:
        db.add(
            models.SalesAgreementItem(
                agreement_id=db_obj.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
        )

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_sales_agreement(db: Session, db_obj: models.SalesAgreement):
    db.delete(db_obj)
    db.commit()
