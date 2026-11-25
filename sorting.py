def merge_sort_parcels(parcels, key_fn=lambda p: (-p["priority"], p["deadline"])):
    """
    Sorts a list of parcel dictionaries using Merge Sort.
    Default order: highest priority first (-priority), then earliest deadline first.
    Time Complexity: O(n log n) | Space Complexity: O(n)
    """
    if len(parcels) <= 1:
        return parcels[:]

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid], key_fn)
    right = merge_sort_parcels(parcels[mid:], key_fn)

    return _merge(left, right, key_fn)


def _merge(left, right, key_fn):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key_fn(left[i]) <= key_fn(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged