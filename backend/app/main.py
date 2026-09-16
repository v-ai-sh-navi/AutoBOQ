from collections import Counter
from pathlib import Path
from app.parser.measurements import extract_measurements
from app.parser.structural_elements import extract_structural_candidates
from app.parser.quantity_engine import calculate_quantities
import tempfile

import ezdxf
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AutoBOQ API",
    description="Automated structural quantity estimation from CAD drawings",
    version="0.1.0"
)


# Allow the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "project": "AutoBOQ",
        "status": "in development"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/drawings/analyze")
async def analyze_drawing(
    file: UploadFile = File(...),
    scale: int = Form(50),
    thickness_m: float = Form(0.20)
):
    if not file.filename.lower().endswith(".dxf"):
        return {
            "error": "Only DXF files are currently supported"
        }

    file_bytes = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".dxf"
    ) as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        doc = ezdxf.readfile(temp_path)
        modelspace = doc.modelspace()

        layers = sorted({
            entity.dxf.layer
            for entity in modelspace
            if hasattr(entity.dxf, "layer")
        })

        entity_types = Counter(
            entity.dxftype()
            for entity in modelspace
        )

        # Geometry extraction
        measurements = extract_measurements(doc)

        total_measured_length = sum(
            measurement["length"]
            for measurement in measurements
        )

        # Structural candidate extraction
        from app.parser.shapes import extract_closed_shapes

        shapes = extract_closed_shapes(doc)

        candidates = extract_structural_candidates(shapes)

        # Quantity calculation
        quantities = calculate_quantities(
            candidates,
            scale=scale,
            thickness_m=thickness_m
        )

        return {
            "filename": file.filename,
            "status": "processed",

            "entity_count": len(modelspace),
            "layer_count": len(layers),
            "layers": layers,
            "entity_types": dict(entity_types),

            "measured_segments": len(measurements),
            "total_measured_length": round(
                total_measured_length, 2
            ),

            "scale": scale,
            "thickness_m": thickness_m,

            "valid_closed_shapes": len(shapes),
            "structural_candidates": len(candidates),

            "quantity_estimate": quantities
        }

    finally:
        Path(temp_path).unlink(missing_ok=True)