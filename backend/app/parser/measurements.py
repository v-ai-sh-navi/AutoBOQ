import math


def extract_measurements(doc):
    measurements = []

    for entity in doc.modelspace():

        if entity.dxftype() == "LWPOLYLINE":

            points = list(entity.get_points())

            for i in range(len(points) - 1):
                x1, y1 = points[i][0], points[i][1]
                x2, y2 = points[i + 1][0], points[i + 1][1]

                length = math.sqrt(
                    (x2 - x1) ** 2 +
                    (y2 - y1) ** 2
                )

                if length >= 0.05:
                    measurements.append({
                    "type": "polyline_segment",
                    "layer": entity.dxf.layer,
                    "length": length
                })

    return measurements