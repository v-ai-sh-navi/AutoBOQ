import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [scale, setScale] = useState(50);
  const [thickness, setThickness] = useState(0.2);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeDrawing = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);
    formData.append("scale", scale);
    formData.append("thickness_m", thickness);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/drawings/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok || data.error) {
        setResult({
          error: data.error || "Analysis failed.",
        });
      } else {
        setResult(data);
      }
    } catch (error) {
      setResult({
        error: "Could not connect to AutoBOQ backend.",
      });
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <header>
        <h1>AutoBOQ</h1>
        <p>
          Automated Structural Quantity Estimation from CAD Drawings
        </p>
      </header>

      <main>

        {/* Upload Section */}
        <div className="upload-card">

          <h2>Analyze CAD Drawing</h2>

          <input
            type="file"
            accept=".dxf"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setResult(null);
            }}
          />

          {file && (
            <p className="filename">
              Selected: <strong>{file.name}</strong>
            </p>
          )}

          <div className="inputs">

            <div>
              <label>Drawing Scale</label>

              <select
                value={scale}
                onChange={(e) => setScale(Number(e.target.value))}
              >
                <option value={20}>1:20</option>
                <option value={25}>1:25</option>
                <option value={50}>1:50</option>
                <option value={100}>1:100</option>
              </select>
            </div>

            <div>
              <label>Assumed Thickness (m)</label>

              <input
                type="number"
                min="0.01"
                step="0.01"
                value={thickness}
                onChange={(e) => setThickness(Number(e.target.value))}
              />
            </div>

          </div>

          <button
            onClick={analyzeDrawing}
            disabled={!file || loading}
          >
            {loading ? "Analyzing..." : "Analyze Drawing"}
          </button>

        </div>


        {/* Results */}
        {result && !result.error && (

          <>

            {/* Overview */}
            <div className="result-card">

              <h2>Drawing Analysis</h2>

              <div className="stats-grid">

                <div className="stat">
                  <span>Entities</span>
                  <strong>{result.entity_count}</strong>
                </div>

                <div className="stat">
                  <span>Layers</span>
                  <strong>{result.layer_count}</strong>
                </div>

                <div className="stat">
                  <span>Closed Shapes</span>
                  <strong>{result.valid_closed_shapes}</strong>
                </div>

                <div className="stat">
                  <span>Structural Candidates</span>
                  <strong>{result.structural_candidates}</strong>
                </div>

              </div>

            </div>


            {/* Quantity Summary */}
            <div className="result-card">

              <h2>Quantity Estimate</h2>

              <div className="quantity-summary">

                <div>
                  <span>Estimated Concrete Volume</span>

                  <strong>
                    {result.quantity_estimate?.total_volume_m3?.toFixed(2)}
                    {" "}m³
                  </strong>
                </div>

                <div>
                  <span>Candidate Elements</span>

                  <strong>
                    {result.quantity_estimate?.total_items}
                  </strong>
                </div>

              </div>

              <p className="assumption">
                Scale: 1:{result.scale} &nbsp; | &nbsp;
                Assumed thickness: {result.thickness_m} m
              </p>

            </div>

            {/* BOQ Summary */}
            <div className="result-card">

              <h2>BOQ Summary</h2>

              <div className="table-container">

                  <table>

                    <thead>
        <tr>
          <th>Description</th>
          <th>Length (m)</th>
          <th>Width (m)</th>
          <th>Thickness (m)</th>
          <th>Quantity</th>
          <th>Volume (m³)</th>
        </tr>
      </thead>

      <tbody>

        {result.quantity_estimate?.boq_summary?.map(
          (item, index) => (

            <tr key={index}>

              <td>{item.description}</td>

              <td>{item.length_m.toFixed(2)}</td>

              <td>{item.width_m.toFixed(2)}</td>

              <td>{item.thickness_m.toFixed(2)}</td>

              <td>{item.quantity}</td>

              <td>{item.volume_m3.toFixed(4)}</td>

            </tr>

          )
        )}

      </tbody>

    </table>

  </div>

</div>


            {/* Quantity Table */}
            <div className="result-card">

              <h2>Quantity Details</h2>

              <div className="table-container">

                <table>

                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Length (m)</th>
                      <th>Width (m)</th>
                      <th>Thickness (m)</th>
                      <th>Volume (m³)</th>
                      <th>Aspect Ratio</th>
                    </tr>
                  </thead>

                  <tbody>

                    {result.quantity_estimate?.items?.map((item) => (

                      <tr key={item.id}>

                        <td>{item.id}</td>

                        <td>{item.length_m.toFixed(3)}</td>

                        <td>{item.width_m.toFixed(3)}</td>

                        <td>{item.thickness_m.toFixed(2)}</td>

                        <td>{item.volume_m3.toFixed(4)}</td>

                        <td>{item.aspect_ratio.toFixed(2)}</td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            </div>


            {/* Technical Information */}
            <div className="result-card">

              <h2>CAD Information</h2>

              <p>
                <strong>File:</strong> {result.filename}
              </p>

              <p>
                <strong>Measured Segments:</strong>{" "}
                {result.measured_segments}
              </p>

              <p>
                <strong>Total Measured Length:</strong>{" "}
                {result.total_measured_length}
              </p>

              <h3>Layers</h3>

              <ul>
                {result.layers?.map((layer) => (
                  <li key={layer}>{layer}</li>
                ))}
              </ul>

              <h3>Entity Types</h3>

              <ul>
                {Object.entries(result.entity_types || {}).map(
                  ([type, count]) => (
                    <li key={type}>
                      {type}: {count}
                    </li>
                  )
                )}
              </ul>

            </div>

          </>

        )}


        {/* Error */}
        {result?.error && (

          <div className="result-card error">
            <strong>Error:</strong> {result.error}
          </div>

        )}

      </main>

    </div>
  );
}

export default App;