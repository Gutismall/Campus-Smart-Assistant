def get_entity_or_404(db, model, item_id: int):
    from fastapi import HTTPException
    entity = db.query(model).filter(model.id == item_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return entity

def delete_entity(db, model, item_id: int):
    entity = get_entity_or_404(db, model, item_id)
    db.delete(entity)
    db.commit()
    return {"message": f"{model.__name__} deleted successfully"}

def update_entity(db, entity, update_data: dict):
    for key, value in update_data.items():
        setattr(entity, key, value)
    db.commit()
    db.refresh(entity)
    return entity
