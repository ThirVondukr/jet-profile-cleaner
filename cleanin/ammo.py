from collections import defaultdict
from typing import List

from typing_extensions import DefaultDict


def clean(profile: dict) -> dict:
    cartridges: DefaultDict[str, list] = defaultdict(list)
    items = profile["Inventory"]["items"]
    for item in items:
        if "slotId" in item and item["slotId"] == "cartridges":
            cartridges[item["parentId"]].append(item)

    broken_ammo: List[dict] = []
    for parent_id, ammo_list in cartridges.items():
        try:
            locations = [ammo["location"] for ammo in ammo_list]
        except KeyError:
            broken_ammo.extend(ammo_list)
            continue

        if sorted(locations) != list(range(len(locations))):
            broken_ammo.extend(ammo_list)

    profile["Inventory"]["items"] = [item for item in profile["Inventory"]["items"] if item not in broken_ammo]

    return profile
