from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository
from schemas.item import ItemCreate, ItemUpdate, Item

class ItemService:
    def __init__(self, db: Session):
        self.item_repository = ItemRepository(db)

    def get_item(self, item_id: int) -> Item | None:
        return self.item_repository.get_item(item_id)

    def get_items(self, skip: int = 0, limit: int = 100) -> list[Item]:
        return self.item_repository.get_items(skip, limit)

    def create_item(self, item: ItemCreate) -> Item:
        return self.item_repository.create_item(item)

    def update_item(self, item_id: int, item_update: ItemUpdate) -> Item | None:
        return self.item_repository.update_item(item_id, item_update)

    def delete_item(self, item_id: int) -> bool:
        return self.item_repository.delete_item(item_id)