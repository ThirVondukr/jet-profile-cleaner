import collections
from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class ProfileCleaningResponse:
    profile: dict
    removed_items_count: int = 0
    duplicate_items: List[str] = field(default_factory=list)
    removed_orphan_items: List[str] = field(default_factory=list)


def clean(profile: dict) -> ProfileCleaningResponse:
    response = ProfileCleaningResponse(profile=profile)
    
    ids_counter = collections.Counter(item["_id"] for item in profile["Inventory"]["items"])
    duplicate_ids: Set[str] = {item_id for item_id, count in ids_counter.items() if count >= 2}
    response.duplicate_items = list(duplicate_ids)

    items = {item["_id"]: item for item in profile["Inventory"]["items"] if item["_id"] not in duplicate_ids}
    response.removed_items_count += len(profile['Inventory']['items']) - len(items)

    # Set of root ids (Stash, quest items, equipment)
    inventory_root_items: Set[str] = {item for item in profile["Inventory"].values() if isinstance(item, str)}

    def is_orphan(item: dict):
        if "parentId" not in item:
            return False

        return item["parentId"] not in items and item["parentId"] not in inventory_root_items

    # Remove orphan items
    while True:
        items_size = len(items)
        response.removed_orphan_items.extend(item["_id"] for item in items.values() if is_orphan(item))
        items = {item_id: item for item_id, item in items.items() if not is_orphan(item)}
        if len(items) == items_size:
            break

    profile["Inventory"]["items"] = list(items.values())

    return response
