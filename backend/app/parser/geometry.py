def extract_polylines(doc):
    polylines = []

    for entity in doc.modelspace():
        if entity.dxftype() == "LWPOLYLINE":
            points = []

            for point in entity.get_points():
                points.append({
                    "x": point[0],
                    "y": point[1]
                })

            polylines.append({
                "layer": entity.dxf.layer,
                "closed": entity.closed,
                "points": points
            })

    return polylines