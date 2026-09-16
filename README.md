# AutoBOQ

### Automated Structural Quantity Estimation from CAD Drawings

AutoBOQ is an ongoing full-stack application for extracting geometric information from CAD/DXF drawings and automating structural quantity-estimation workflows.

The project combines Civil Engineering domain knowledge with CAD processing, data handling, REST APIs, and a web-based interface.

## Current Architecture

CAD / DXF Drawing → ezdxf Parser → Geometry Extraction → Structural Element Detection → Quantity Estimation Engine → FastAPI → React UI

## Tech Stack

Backend:
- Python
- FastAPI
- ezdxf
- Pandas
- Uvicorn

Frontend:
- React
- JavaScript
- Vite
- CSS

Development:
- Git
- GitHub

Planned:
- PostgreSQL
- BOQ export
- Excel/PDF reporting
- Improved structural element classification

## Current Features

- DXF file upload through a web interface
- CAD entity extraction using ezdxf
- Layer and entity-type analysis
- Closed-shape detection
- Geometric dimension extraction
- Structural geometry candidate identification
- Quantity estimation based on drawing scale and assumed thickness
- BOQ-style quantity summary
- REST API using FastAPI
- React-based frontend
- End-to-end communication between frontend and backend

## Example Processing

A structural DXF drawing can be uploaded through the application.

The backend processes the drawing and extracts information such as:

- Total CAD entities
- Layers
- Entity types
- Closed geometric shapes
- Structural geometry candidates
- Estimated dimensions
- Estimated concrete volume

The results are returned through the FastAPI endpoint and displayed in the React interface.

## Project Status

Ongoing

The current implementation establishes the CAD processing and quantity-estimation pipeline. Further development will focus on improving structural element classification, persistent data storage, and BOQ/report generation.

## Running Locally

Backend:

cd backend

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn app.main:app --reload

API:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

Frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The React application will be available at the local Vite URL shown in the terminal.

## Project Structure
'''

AutoBOQ/
├── backend/
│   ├── app/
│   │   ├── parser/
│   │   │   ├── dxf_parser.py
│   │   │   ├── geometry.py
│   │   │   ├── measurements.py
│   │   │   ├── shapes.py
│   │   │   ├── structural_elements.py
│   │   │   └── quantity_engine.py
│   │   └── main.py
│   ├── requirements.txt
│   └── test_parser.py
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── index.css
├── data/
│   └── sample_structural.dxf
└── README.md
'''
## Note

The current quantity estimates are based on extracted geometry, drawing scale, and user-provided assumptions. They are intended as a development-stage estimation workflow and should not be treated as final engineering BOQ quantities.

## Future Development

- PostgreSQL integration for storing drawing analyses
- Improved structural member recognition
- Beam, column, slab, and footing classification
- More robust drawing-unit and scale handling
- Detailed BOQ generation
- Excel and PDF export
- Quantity calculation audit trail
- Drawing-level analysis history
