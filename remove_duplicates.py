import collections
from dataclasses import dataclass
from typing import Final, Set


@dataclass
class ProfileCleaningResponse:
    profile: dict
    duplicate_ids: int
    items_removed: int


def clean(profile: dict) -> ProfileCleaningResponse:
    ids_counter = collections.Counter(item["_id"] for item in profile["Inventory"]["items"])
    duplicate_ids: Set[str] = {item_id for item_id, count in ids_counter.items() if count >= 2}

    items_before: Final[int] = len(profile["Inventory"]["items"])

    items = {item["_id"]: item for item in profile["Inventory"]["items"] if item["_id"] not in duplicate_ids}

    # Set of root ids (Stash, quest items, equipment)
    inventory_root_items: Set[str] = {item for item in profile["Inventory"].values() if isinstance(item, str)}
    # Remove orphan items
    while True:
        items_size = len(items)
        items = {
            item_id: item
            for item_id, item in items.items()
            if "parentId" not in item or item["parentId"] in items or item["parentId"] in inventory_root_items
        }
        if len(items) == items_size:
            break

    profile["Inventory"]["items"] = list(items.values())
    return ProfileCleaningResponse(
        profile=profile,
        duplicate_ids=len(duplicate_ids),
        items_removed=items_before - len(profile["Inventory"]["items"]),
    )
