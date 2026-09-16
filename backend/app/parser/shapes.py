def extract_closed_shapes(doc):
    shapes = []

    for entity in doc.modelspace():

        if entity.dxftype() != "LWPOLYLINE":
            continue

        if not entity.closed:
            continue

        points = list(entity.get_points())

        if len(points) < 3:
            continue

        xs = [point[0] for point in points]
        ys = [point[1] for point in points]

        width = float(max(xs) - min(xs))
        height = float(max(ys) - min(ys))

        # Ignore degenerate geometry
        if width < 0.01 or height < 0.01:
            continue

        shapes.append({
            "layer": entity.dxf.layer,
            "point_count": len(points),
            "width": width,
            "height": height,
            "area": width * height
        })

    return shapes