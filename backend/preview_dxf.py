import ezdxf
import matplotlib.pyplot as plt

doc = ezdxf.readfile("../data/sample_structural.dxf")
msp = doc.modelspace()

fig, ax = plt.subplots()

for entity in msp:
    if entity.dxftype() == "LWPOLYLINE":
        points = entity.get_points()

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        ax.plot(xs, ys, linewidth=0.3)

ax.set_aspect("equal")
ax.set_title("AutoBOQ - CAD Geometry Preview")

plt.savefig("../data/dxf_preview.png", dpi=200)
plt.close()

print("Preview saved to ../data/dxf_preview.png")