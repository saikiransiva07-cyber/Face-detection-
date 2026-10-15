# SYSTEM // OPTICS-04: Face Localization and Privacy Analytics

`OPTICS-04` is an industrial-grade face localization and optical privacy analytics console implemented in Python with Streamlit and OpenCV. Designed in accordance with Swiss Editorial Typography and hardware instrument interface principles (referencing Leica optical rangefinders and Teenage Engineering telemetry systems), the platform executes real-time facial feature isolation, metric spatial quantification, and redaction masking.

---

## Technical Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│ MASTHEAD // SYSTEM SPECIFICATION & TEMPORAL CLOCK                      │
├──────────────────────────────────────┬─────────────────────────────────┤
│ OPTICAL VIEWFINDER (70% WIDTH)       │ TELEMETRY LEDGER (30% WIDTH)    │
│                                      │                                 │
│ - Multi-source Ingestion:            │ - Optical Calibration Matrix    │
│   • Sensor Benchmarks (Solo / Duo)   │ - Metric Gauges:                │
│   • Direct File Upload (JPG/PNG)     │   • Subject Count               │
│   • Optical Camera Stream            │   • Sensor Resolution           │
│ - Corner Crosshair Overlays          │   • Field Scan Latency (ms)     │
│ - Dynamic Monospace Tags             │   • Spatial Density (%)         │
│ - Coordinate Telemetry Readouts      │ - Target Coordinate Ledger      │
│                                      │ - Structured Log Export (.CSV)  │
│                                      │ - Optical Frame Export (.PNG)   │
└──────────────────────────────────────┴─────────────────────────────────┘
```

---

## Design System Specifications

The visual interface is engineered to eliminate decorative conventions, rounded pill buttons, glowing drop shadows, and neon gradients in favor of an ergonomic, high-density telemetry layout.

- **Color Palette (Warm Paper & Carbon):**
  - Background: Matte Warm Stone (`#F4F3EF`)
  - Ink & Structural Lines: Deep Charcoal (`#141413`)
  - Hairline Partition Borders: Precision Light Stone (`#D6D4CE`)
  - Viewfinder Surface: Matte Aluminum Tint (`#EAE8E2`)
  - Active State & Target Reticles: International Signal Orange (`#FF4F00`)
- **Typography:**
  - Display and Section Nomenclature: `Space Grotesk`
  - Telemetry Data, Coordinates, and System Micro-labels: `JetBrains Mono`
  - Micro-label Format: Uppercase monospace, `11px`, letter-spacing `0.08em`, color `#6C6B66`
- **Component Geometry:** Sharp `2px` corners, `1px` structural borders, zero drop shadows.
- **Suppressed Chrome:** Streamlit default headers, footers, status widgets, and excessive padding are stripped via injected CSS style blocks.

---

## Optical Pipeline Modes

The console features three distinct operational pipelines:

### 1. RAW_DETECTION
Standard optical sensor pass with high-precision reticle overlays.
- Reticle geometry: Ultra-thin `1px` corner ticks at four quadrant vertices rather than full solid perimeter boxes.
- Sub-pixel center crosshairs at detected region centroids.
- Solid Signal Orange ID badge (`SUBJ_01`, `SUBJ_02`) with dark charcoal typography in `FONT_HERSHEY_PLAIN`.
- Coordinate readout formatted as `[X:### Y:###]` adjacent to the identifier badge.

### 2. REDACTION_MASK
Editorial documentary privacy censorship block.
- Applies a high-contrast pixelated mosaic transformation over detected regions of interest (ROI).
- Retains corner reticle brackets and tags the subject as `REDACTED_##` in Signal Orange.
- Configurable mosaic block granularity (`8px` to `48px`).

### 3. HIGH_CONTRAST_MONO
Simulates a high-contrast black-and-white analog emulsion (Leica Monochrom / Kodak Tri-X 400).
- Desaturates frame, enhances micro-contrast via S-curve tone mapping, and introduces procedural analog film grain.
- Overlays International Signal Orange (`#FF4F00`) targeting reticles directly onto the monochrome image, creating stark visual separation between telemetry and photographic subject.

---

## Telemetry Metrics and Export Schema

The telemetry engine calculates frame metrics in real time:

- **Subject Count:** Total isolated facial structures within the frame.
- **Sensor Resolution:** Width × Height in pixels.
- **Processing Time:** Execution latency of the Haar cascade detector in milliseconds.
- **Spatial Density:** Proportion of the total frame surface area occupied by detected subjects:
  $$\text{Spatial Density (\%)} = \left( \frac{\sum_{i=1}^{N} (w_i \times h_i)}{W_{\text{frame}} \times H_{\text{frame}}} \right) \times 100$$

### CSV Export Schema

Exported field logs adhere to the following schema:

| Column Header | Data Type | Description |
| :--- | :--- | :--- |
| `TIMESTAMP_UTC` | String | ISO 8601 UTC timestamp of frame capture |
| `SUBJECT_ID` | String | Identifier tag (`SUBJ_01` or `REDACTED_01`) |
| `ORIGIN_X_PX` | Integer | X coordinate of the top-left vertex |
| `ORIGIN_Y_PX` | Integer | Y coordinate of the top-left vertex |
| `WIDTH_PX` | Integer | Bounding width in pixels |
| `HEIGHT_PX` | Integer | Bounding height in pixels |
| `AREA_PX2` | Integer | Bounding area ($w \times h$) in square pixels |
| `FRAME_WIDTH_PX` | Integer | Frame horizontal resolution |
| `FRAME_HEIGHT_PX` | Integer | Frame vertical resolution |
| `SPATIAL_COVERAGE_PCT` | Float | Percentage of frame area occupied by subject |
| `PIPELINE_MODE` | String | Active processing mode (`RAW_DETECTION`, etc.) |
| `PROCESSING_TIME_MS` | Float | Cascade detection execution time in milliseconds |

---

## Installation & Deployment

### Prerequisites
- Python 3.10 to 3.12
- Operating System: macOS, Linux, or Windows

### Local Setup

1. Clone or extract the repository:
   ```bash
   git clone https://github.com/suryaprakash-tech/Face-Detection.git
   cd Face-Detection
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application:
   ```bash
   streamlit run app.py
   ```

5. Access the console via your local browser at `http://localhost:8501`.

---

## Repository Structure

```text
.
├── assets/
│   ├── benchmark_01.jpg      # Standard test portrait (solo subject)
│   └── benchmark_02.jpg      # Multi-subject test pattern (duo subjects)
├── app.py                    # Main application code and pipeline orchestration
├── packages.txt              # Debian/Ubuntu system libraries (libgl1, libglib2.0-0)
├── requirements.txt          # Python package manifest
├── runtime.txt               # Platform runtime version specification (python-3.12)
└── README.md                 # System technical documentation
```

---

## License

This software is distributed under the MIT License. See `LICENSE` for details.

