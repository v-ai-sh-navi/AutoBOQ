from collections import defaultdict


def calculate_quantities(
    candidates,
    scale=50,
    paper_unit_to_meter=0.0254,
    thickness_m=0.20
):
    results = []

    for candidate in candidates:

        length_m = (
            candidate["long_side"]
            * scale
            * paper_unit_to_meter
        )

        width_m = (
            candidate["short_side"]
            * scale
            * paper_unit_to_meter
        )

        volume_m3 = (
            length_m
            * width_m
            * thickness_m
        )

        results.append({
            "id": candidate["id"],
            "source_layer": candidate["source_layer"],
            "drawing_length": round(
                candidate["long_side"], 4
            ),
            "drawing_width": round(
                candidate["short_side"], 4
            ),
            "length_m": round(length_m, 3),
            "width_m": round(width_m, 3),
            "thickness_m": thickness_m,
            "volume_m3": round(volume_m3, 4),
            "aspect_ratio": round(
                candidate["aspect_ratio"], 2
            )
        })

    # ---------------------------------
    # BOQ aggregation
    # ---------------------------------

    grouped = defaultdict(lambda: {
        "quantity": 0,
        "total_volume_m3": 0.0
    })

    for item in results:

        # Round dimensions so tiny floating-point
        # differences don't create separate BOQ rows.
        key = (
            round(item["length_m"], 2),
            round(item["width_m"], 2),
            round(item["thickness_m"], 2)
        )

        grouped[key]["quantity"] += 1
        grouped[key]["total_volume_m3"] += item["volume_m3"]

    boq_items = []

    for key, data in grouped.items():

        length_m, width_m, thickness = key

        boq_items.append({
            "description": "Structural candidate",
            "length_m": length_m,
            "width_m": width_m,
            "thickness_m": thickness,
            "quantity": data["quantity"],
            "volume_m3": round(
                data["total_volume_m3"], 4
            )
        })

    boq_items.sort(
        key=lambda item: item["volume_m3"],
        reverse=True
    )

    total_volume = sum(
        item["volume_m3"]
        for item in boq_items
    )

    return {
        "items": results,
        "total_items": len(results),
        "total_volume_m3": round(total_volume, 4),
        "boq_summary": boq_items
    }