import ezdxf

from app.parser.shapes import extract_closed_shapes
from app.parser.structural_elements import extract_structural_candidates
from app.parser.quantity_engine import calculate_quantities


doc = ezdxf.readfile("../data/sample_structural.dxf")

shapes = extract_closed_shapes(doc)

candidates = extract_structural_candidates(shapes)

quantities = calculate_quantities(
    candidates,
    scale=50,
    thickness_m=0.20
)

print("Valid closed shapes:", len(shapes))
print("Structural candidates:", len(candidates))

print("\nFirst 10 quantity results:")

for item in quantities["items"][:10]:
    print(item)

print("\nTOTAL")
print("Items:", quantities["total_items"])
print("Estimated volume:", quantities["total_volume_m3"], "m3")