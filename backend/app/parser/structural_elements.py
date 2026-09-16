def extract_structural_candidates(shapes):
    candidates = []

    for index, shape in enumerate(shapes, start=1):

        width = shape["width"]
        height = shape["height"]

        if width <= 0 or height <= 0:
            continue

        long_side = max(width, height)
        short_side = min(width, height)

        aspect_ratio = long_side / short_side

        # Ignore extremely large sheet/drawing boundaries
        if long_side > 10:
            continue

        # Simple rectangular geometry candidates
        if shape["point_count"] not in [4, 5]:
            continue

        if aspect_ratio < 1.5 or aspect_ratio > 20:
            continue

        candidates.append({
            "id": f"CAND-{index:04d}",
            "source_layer": shape["layer"],
            "width": width,
            "height": height,
            "long_side": long_side,
            "short_side": short_side,
            "aspect_ratio": aspect_ratio,
            "geometry_area": shape["area"]
        })

    return candidates