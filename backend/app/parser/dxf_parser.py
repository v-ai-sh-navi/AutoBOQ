import ezdxf


def parse_dxf(file_path):
    doc = ezdxf.readfile(file_path)

    layers = []

    for layer in doc.layers:
        layers.append(layer.dxf.name)

    entities = []

    for entity in doc.modelspace():
        entities.append({
            "type": entity.dxftype(),
            "layer": entity.dxf.layer
        })

    return {
        "layers": layers,
        "entity_count": len(entities),
        "entities": entities
    }