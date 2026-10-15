import io
import os
import time
from datetime import datetime, timezone

import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

# ==============================================================================
# INDUSTRIAL INTERFACE CONFIGURATION // SWISS EDITORIAL ARCHITECTURE
# ==============================================================================

st.set_page_config(
    page_title="SYSTEM // OPTICS-04",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Color Palette: Warm Paper & Carbon
# Background: #F4F3EF (Matte Warm Stone)
# Text & Structural Borders: #141413 (Deep Charcoal Ink), #D6D4CE (Hairline Border)
# Signal Accent: #FF4F00 (International Signal Orange)

INJECTED_CSS = """
<style>

/* Reset and suppress Streamlit chrome */
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}

html, body, [class*="css"], .stApp {
    background-color: #F4F3EF !important;
    color: #141413 !important;
    font-family: 'Space Grotesk', 'Trebuchet MS', sans-serif !important;
    letter-spacing: 0;
}

/* Base Container layout */
.block-container {
    max-width: 100% !important;
    padding-top: 1.25rem !important;
    padding-bottom: 2.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Typography tokens */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: #141413 !important;
    letter-spacing: -0.02em !important;
    text-transform: uppercase;
}

.mono {
    font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, monospace !important;
}

/* Masthead Grid */
.masthead-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 2px solid #141413;
    border-bottom: 1px solid #141413;
    padding: 0.85rem 0;
    margin-bottom: 1.5rem;
    background-color: #F4F3EF;
    gap: 1rem;
    flex-wrap: wrap;
}

.masthead-col {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.masthead-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #141413;
    letter-spacing: 0.05em;
    line-height: 1.1;
}

.micro-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6C6B66;
    line-height: 1;
}

.mono-readout {
    font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, monospace;
    font-size: 0.85rem;
    font-weight: 500;
    color: #141413;
    letter-spacing: 0.02em;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #141413;
    text-transform: uppercase;
}

.status-indicator-sq {
    width: 8px;
    height: 8px;
    background-color: #FF4F00;
    display: inline-block;
}

/* Viewfinder container frame */
.viewfinder-card {
    border: 1px solid #141413;
    background-color: #EAE8E2;
    padding: 0;
    position: relative;
    margin-bottom: 1rem;
}

.viewfinder-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0.75rem;
    background-color: #141413;
    color: #F4F3EF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.08em;
}

.viewfinder-bar-subtle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 0.75rem;
    border-top: 1px solid #D6D4CE;
    background-color: #F4F3EF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #6C6B66;
    letter-spacing: 0.06em;
}

/* Telemetry Section and Cards */
.telemetry-section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #141413;
    border-bottom: 1px solid #141413;
    padding-bottom: 4px;
    margin-bottom: 0.75rem;
}

.spec-grid {
    display: block;
    margin-bottom: 1.25rem;
}

.spec-box {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.75rem;
    border: 0;
    border-bottom: 1px solid #D6D4CE;
    background: transparent;
    padding: 0.65rem 0;
    border-radius: 0;
}

.spec-box:first-child {
    border-top: 1px solid #D6D4CE;
    border-left: 2px solid #FF4F00;
    padding-left: 0.55rem;
}

.spec-val {
    font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #141413;
    line-height: 1.1;
    white-space: nowrap;
}

.spec-val-sm {
    font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, monospace;
    font-size: 0.9rem;
    font-weight: 600;
    color: #141413;
    line-height: 1.1;
    white-space: nowrap;
}

/* Sharp UI Controls & Form elements */
div[data-baseweb="tab-list"] {
    background-color: transparent !important;
    gap: 4px !important;
    border-bottom: 1px solid #D6D4CE !important;
}

button[data-baseweb="tab"] {
    border-radius: 2px 2px 0 0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1rem !important;
    background-color: #EAE8E2 !important;
    color: #6C6B66 !important;
    border: 1px solid #D6D4CE !important;
    border-bottom: none !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #141413 !important;
    color: #F4F3EF !important;
    border-color: #141413 !important;
}

/* Streamlit Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 2px !important;
    border: 1px solid #141413 !important;
    background-color: #141413 !important;
    color: #F4F3EF !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    box-shadow: none !important;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #FF4F00 !important;
    border-color: #FF4F00 !important;
    color: #FFFFFF !important;
}

/* Secondary Button styling */
.secondary-btn > div > button {
    background-color: #FFFFFF !important;
    color: #141413 !important;
    border: 1px solid #D6D4CE !important;
}
.secondary-btn > div > button:hover {
    background-color: #141413 !important;
    color: #FFFFFF !important;
    border-color: #141413 !important;
}

/* Sliders */
div[data-testid="stSlider"] {
    margin-bottom: 0.6rem;
}

div[data-testid="stSlider"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #6C6B66 !important;
}

div[data-testid="stSlider"] div[role="slider"] {
    background-color: #FF4F00 !important;
    border: 2px solid #141413 !important;
    border-radius: 2px !important;
    width: 14px !important;
    height: 14px !important;
    box-shadow: none !important;
}

div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
    background-color: #FF4F00 !important;
}

/* Radio buttons & Mode selection */
div[data-testid="stRadio"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    color: #141413 !important;
}

div[data-testid="stRadio"] > div {
    gap: 8px !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label {
    background: transparent;
    border: 1px solid transparent;
    border-bottom-color: #D6D4CE;
    padding: 0.45rem 0.65rem;
    border-radius: 0;
    margin-bottom: 0;
    transition: background-color 0.15s ease, color 0.15s ease;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    border-color: #141413;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label,
div[data-testid="stRadio"] div[role="radiogroup"] > label p {
    color: #141413 !important;
    opacity: 1 !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: #141413;
    border-color: #141413;
    color: #F4F3EF !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p,
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span {
    color: #F4F3EF !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) > div:first-child {
    border-color: #FF4F00 !important;
    background-color: #FF4F00 !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) > div:first-child > div {
    border-color: #FF4F00 !important;
    background-color: #FF4F00 !important;
}

div[data-testid="stImage"] img {
    border-radius: 0 !important;
}

/* File Uploader & Camera */
div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
    border-radius: 2px !important;
}

div[data-testid="stFileUploader"] section {
    background-color: #FFFFFF !important;
    border: 1px dashed #141413 !important;
    border-radius: 2px !important;
    padding: 1rem !important;
}

div[data-testid="stFileUploader"] section button {
    border-radius: 2px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    border: 1px solid #141413 !important;
}

/* Data Table Ledger */
.ledger-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    background-color: #FFFFFF;
    border: 1px solid #D6D4CE;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    display: block;
    overflow-x: auto;
    white-space: nowrap;
}

@media (max-width: 760px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .masthead-container {
        align-items: flex-start;
    }

    .masthead-col {
        min-width: 45%;
    }
}

.ledger-table th {
    background-color: #141413;
    color: #F4F3EF;
    text-align: left;
    padding: 6px 8px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 10px;
    border: 1px solid #141413;
}

.ledger-table td {
    padding: 6px 8px;
    border-bottom: 1px solid #EAE8E2;
    border-right: 1px solid #EAE8E2;
    color: #141413;
    letter-spacing: 0.02em;
}

.ledger-table tr:last-child td {
    border-bottom: none;
}

.tag-badge {
    background-color: #FF4F00;
    color: #FFFFFF;
    padding: 2px 5px;
    font-weight: 700;
    font-size: 10px;
    display: inline-block;
    border-radius: 1px;
}

.status-locked {
    color: #141413;
    font-weight: 600;
}

.status-redacted {
    color: #FF4F00;
    font-weight: 600;
}

/* Callout panel */
.callout-box {
    border: 1px solid #D6D4CE;
    border-left: 3px solid #141413;
    background-color: #FFFFFF;
    padding: 0.65rem 0.85rem;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #141413;
    line-height: 1.4;
}

.callout-box-alert {
    border-left-color: #FF4F00;
}
</style>
"""

st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
""",
    unsafe_allow_html=True,
)
st.markdown(INJECTED_CSS, unsafe_allow_html=True)

# OPENCV CLASSIFIER CACHE & PIPELINE LOGIC

SIGNAL_ORANGE_BGR = (0, 79, 255)  # Hex #FF4F00 in OpenCV BGR
DARK_CHARCOAL_BGR = (19, 20, 20)  # Hex #141413 in OpenCV BGR
WHITE_BGR = (255, 255, 255)


@st.cache_resource
def get_face_detector():
    """Initializes OpenCV Haar Cascade Frontal Face Classifier."""
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    classifier = cv2.CascadeClassifier(cascade_path)
    if classifier.empty():
        raise RuntimeError(f"Failed to load OpenCV Haar Cascade from {cascade_path}")
    return classifier


def detect_faces(image_bgr: np.ndarray, scale_factor: float, min_neighbors: int):
    """
    Executes Haar Cascade face detection on input frame.
    Returns: list of (x, y, w, h) bounding boxes and execution time in milliseconds.
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    detector = get_face_detector()

    t_start = time.perf_counter()
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(28, 28),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    return faces, t_elapsed_ms


def draw_viewfinder_overlay(
    canvas_bgr: np.ndarray,
    faces,
    tag_prefix: str = "SUBJ",
    draw_crosshairs: bool = True,
):
    """
    Renders Swiss/Industrial technical reticles:
    - Ultra-thin 1px corner crosshair ticks.
    - Minimal center crosshair +.
    - Solid Signal Orange tag badge (SUBJ_01).
    - Precision coordinate readout [X:120 Y:84].
    """
    annotated = canvas_bgr.copy()

    for idx, (x, y, w, h) in enumerate(faces):
        subj_id = f"{tag_prefix}_{idx+1:02d}"

        # 1px Corner ticks (proportional to face size, clamp between 10px and 24px)
        tick_len = int(np.clip(min(w, h) * 0.18, 10, 26))

        # Top-Left corner
        cv2.line(annotated, (x, y), (x + tick_len, y), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)
        cv2.line(annotated, (x, y), (x, y + tick_len), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)

        # Top-Right corner
        cv2.line(annotated, (x + w, y), (x + w - tick_len, y), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)
        cv2.line(annotated, (x + w, y), (x + w, y + tick_len), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)

        # Bottom-Left corner
        cv2.line(annotated, (x, y + h), (x + tick_len, y + h), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)
        cv2.line(annotated, (x, y + h), (x, y + h - tick_len), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)

        # Bottom-Right corner
        cv2.line(annotated, (x + w, y + h), (x + w - tick_len, y + h), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)
        cv2.line(annotated, (x + w, y + h), (x + w, y + h - tick_len), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)

        # Subtle center crosshair
        if draw_crosshairs:
            cx, cy = x + w // 2, y + h // 2
            cv2.line(annotated, (cx - 4, cy), (cx + 4, cy), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)
            cv2.line(annotated, (cx, cy - 4), (cx, cy + 4), SIGNAL_ORANGE_BGR, 1, cv2.LINE_AA)

        # Tag Badge calculation
        font = cv2.FONT_HERSHEY_PLAIN
        font_scale = 0.95
        font_thick = 1

        (text_w, text_h), baseline = cv2.getTextSize(subj_id, font, font_scale, font_thick)
        badge_pad_x = 4
        badge_pad_y = 3
        badge_w = text_w + (badge_pad_x * 2)
        badge_h = text_h + (badge_pad_y * 2)

        # Position tag directly above top-left corner, or inside if top margin is insufficient
        if y - badge_h - 2 >= 0:
            bx1, by1 = x, y - badge_h - 2
        else:
            bx1, by1 = x, y + 2

        bx2, by2 = bx1 + badge_w, by1 + badge_h

        # Draw solid Signal Orange badge with Dark Charcoal label
        cv2.rectangle(annotated, (bx1, by1), (bx2, by2), SIGNAL_ORANGE_BGR, -1)
        text_origin = (bx1 + badge_pad_x, by2 - badge_pad_y)
        cv2.putText(annotated, subj_id, text_origin, font, font_scale, DARK_CHARCOAL_BGR, font_thick, cv2.LINE_AA)

        # Coordinate Readout string
        coord_str = f"[X:{x} Y:{y}]"
        coord_x = bx2 + 6
        coord_y = text_origin[1]
        cv2.putText(annotated, coord_str, (coord_x, coord_y), font, font_scale, SIGNAL_ORANGE_BGR, font_thick, cv2.LINE_AA)

    return annotated


def apply_redaction_mask(image_bgr: np.ndarray, faces, mosaic_block_size: int = 16):
    """
    Applies high-contrast pixelated documentary mosaic censor blocks over detected ROIs,
    followed by Signal Orange corner ticks and REDACTED identification tags.
    """
    masked_img = image_bgr.copy()

    for idx, (x, y, w, h) in enumerate(faces):
        # Clip bounding box to frame dimensions
        im_h, im_w = masked_img.shape[:2]
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(im_w, x + w), min(im_h, y + h)

        roi = masked_img[y1:y2, x1:x2]
        roi_h, roi_w = roi.shape[:2]

        if roi_h > 0 and roi_w > 0:
            # Downsample to small grid, then upsample back with nearest-neighbor interpolation
            grid_w = max(1, roi_w // mosaic_block_size)
            grid_h = max(1, roi_h // mosaic_block_size)

            small_roi = cv2.resize(roi, (grid_w, grid_h), interpolation=cv2.INTER_LINEAR)
            pixelated_roi = cv2.resize(small_roi, (roi_w, roi_h), interpolation=cv2.INTER_NEAREST)

            # High-contrast tonal curve on the mosaic for editorial documentary impact
            pixelated_roi = cv2.convertScaleAbs(pixelated_roi, alpha=1.12, beta=-6)
            masked_img[y1:y2, x1:x2] = pixelated_roi

    # Overlay corner reticles and redacted tags
    annotated = draw_viewfinder_overlay(masked_img, faces, tag_prefix="REDACTED", draw_crosshairs=False)
    return annotated


def apply_high_contrast_mono(
    image_bgr: np.ndarray,
    faces,
    grain_sigma: float = 12.0,
    contrast_alpha: float = 1.35,
    brightness_beta: int = -18,
):
    """
    Converts frame to grainy B&W film aesthetic (Leica Monochrom / Tri-X 400 inspired),
    while rendering only the Signal Orange targeting reticles in vivid color.
    """
    # Convert to single-channel grayscale
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Filmic S-curve tone mapping and high contrast
    contrasted = cv2.convertScaleAbs(gray, alpha=contrast_alpha, beta=brightness_beta)

    # Procedural analog film grain
    if grain_sigma > 0.1:
        np.random.seed(42)  # Deterministic seed for visual stability across renders
        noise = np.random.normal(0.0, grain_sigma, gray.shape).astype(np.float32)
        grainy = np.clip(contrasted.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    else:
        grainy = contrasted

    # Reconstitute into 3-channel BGR for color HUD overlay
    mono_bgr = cv2.cvtColor(grainy, cv2.COLOR_GRAY2BGR)

    # Overlay vivid Signal Orange viewfinder reticles onto monochrome frame
    annotated = draw_viewfinder_overlay(mono_bgr, faces, tag_prefix="SUBJ", draw_crosshairs=True)
    return annotated


# ==============================================================================
# IMAGE INGESTION MODULE
# ==============================================================================

BENCHMARK_SOLO_PATH = os.path.join("assets", "benchmark_01.jpg")
BENCHMARK_DUO_PATH = os.path.join("assets", "benchmark_02.jpg")


def load_image_from_source(source_type: str, uploaded_file=None, camera_file=None):
    """Loads and standardizes input frame to OpenCV BGR format."""
    if source_type == "BENCHMARK_01 [SOLO]":
        if os.path.exists(BENCHMARK_SOLO_PATH):
            return cv2.imread(BENCHMARK_SOLO_PATH)
        return None

    elif source_type == "BENCHMARK_02 [DUO]":
        if os.path.exists(BENCHMARK_DUO_PATH):
            return cv2.imread(BENCHMARK_DUO_PATH)
        return None

    elif source_type == "IMAGE_UPLOAD [.JPG / .PNG]" and uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img_bgr

    elif source_type == "OPTICAL_WEBCAM [DIRECT]" and camera_file is not None:
        file_bytes = np.asarray(bytearray(camera_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img_bgr

    return None


# ==============================================================================
# APPLICATION INTERFACE ARCHITECTURE
# ==============================================================================

# Session Timestamp
current_timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

# Optical Mode Session State default
if "active_mode" not in st.session_state:
    st.session_state["active_mode"] = "RAW_DETECTION"

# --- 1. TOP EDITORIAL MASTHEAD ---
st.markdown(
    f"""
<div class="masthead-container">
    <div class="masthead-col" style="flex: 2;">
        <span class="micro-label">SYSTEM IDENTIFIER</span>
        <span class="masthead-title">SYSTEM // OPTICS-04</span>
        <span class="micro-label" style="margin-top: 2px;">SWISS EDITORIAL SPATIAL TELEMETRY & PRIVACY ANALYTICS</span>
    </div>
    <div class="masthead-col" style="flex: 1; border-left: 1px solid #D6D4CE; padding-left: 1.25rem;">
        <span class="micro-label">TEMPORAL TIMESTAMP</span>
        <span class="mono-readout">{current_timestamp_utc}</span>
        <span class="micro-label" style="margin-top: 2px;">CALIBRATION: HAAR_CASCADE_V2</span>
    </div>
    <div class="masthead-col" style="flex: 1; border-left: 1px solid #D6D4CE; padding-left: 1.25rem; align-items: flex-start;">
        <span class="micro-label">PIPELINE STATUS</span>
        <div class="status-pill">
            <span class="status-indicator-sq"></span>
            <span>{st.session_state["active_mode"]} [ACTIVE]</span>
        </div>
        <span class="micro-label" style="margin-top: 2px;">SIGNAL PROTOCOL: BGR_888</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 2. ASYMMETRIC SPLIT WORKSPACE (70% / 30%) ---
col_viewfinder, col_telemetry = st.columns([7, 3], gap="large")

with col_telemetry:
    # Telemetry Ledger Sidebar
    st.markdown('<div class="telemetry-section-title">01 // OPTICAL CALIBRATION & MODE</div>', unsafe_allow_html=True)

    mode_options = ["RAW_DETECTION", "REDACTION_MASK", "HIGH_CONTRAST_MONO"]
    mode_labels = {
        "RAW_DETECTION": "RAW / DETECT",
        "REDACTION_MASK": "REDACTION",
        "HIGH_CONTRAST_MONO": "MONO / GRAIN",
    }
    selected_mode = st.radio(
        label="PROCESSING PIPELINE MODE",
        options=mode_options,
        format_func=lambda mode: mode_labels[mode],
        index=mode_options.index(st.session_state["active_mode"]),
        label_visibility="collapsed",
    )
    st.session_state["active_mode"] = selected_mode

    # Calibration Sliders
    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
    scale_factor = st.slider(
        "SCALE FACTOR (PYRAMID DECIMATION)",
        min_value=1.05,
        max_value=1.35,
        value=1.15,
        step=0.01,
        format="%.2f",
    )

    min_neighbors = st.slider(
        "MINIMUM NEIGHBORS (STABILITY THRESHOLD)",
        min_value=3,
        max_value=9,
        value=5,
        step=1,
    )

    mosaic_size = 16
    grain_intensity = 12.0

    if selected_mode == "REDACTION_MASK":
        mosaic_size = st.slider(
            "CENSOR MOSAIC BLOCK SIZE (PX)",
            min_value=8,
            max_value=48,
            value=18,
            step=2,
        )
    elif selected_mode == "HIGH_CONTRAST_MONO":
        grain_intensity = st.slider(
            "FILM GRAIN DENSITY (SIGMA)",
            min_value=0.0,
            max_value=30.0,
            value=14.0,
            step=1.0,
        )

with col_viewfinder:
    # Optical Viewfinder Source Tabs
    source_labels = {
        "BENCHMARK_01 [SOLO]": "REFERENCE / SOLO",
        "BENCHMARK_02 [DUO]": "REFERENCE / DUO",
        "IMAGE_UPLOAD [.JPG / .PNG]": "UPLOAD IMAGE",
        "OPTICAL_WEBCAM [DIRECT]": "CAMERA CAPTURE",
    }
    source_choice = st.radio(
        label="INPUT SENSOR SELECTION",
        options=list(source_labels),
        format_func=lambda source: source_labels[source],
        horizontal=True,
    )

    uploaded_data = None
    camera_data = None

    if source_choice == "IMAGE_UPLOAD [.JPG / .PNG]":
        uploaded_data = st.file_uploader(
            "SELECT HIGH-RESOLUTION IMAGE FILE",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )
    elif source_choice == "OPTICAL_WEBCAM [DIRECT]":
        camera_data = st.camera_input(
            "OPTICAL SENSOR CAPTURE",
            label_visibility="collapsed",
        )

    # Ingest image
    raw_frame_bgr = load_image_from_source(source_choice, uploaded_data, camera_data)

# Process frame if present
if raw_frame_bgr is not None:
    frame_h, frame_w = raw_frame_bgr.shape[:2]
    frame_area = frame_w * frame_h

    # Detection step
    detected_faces, latency_ms = detect_faces(raw_frame_bgr, scale_factor, min_neighbors)
    subject_count = len(detected_faces)

    # Calculate spatial density
    total_face_area = sum(w * h for (_, _, w, h) in detected_faces)
    spatial_density_pct = (total_face_area / frame_area * 100.0) if frame_area > 0 else 0.0

    # Pipeline Transformation Mode
    if selected_mode == "RAW_DETECTION":
        processed_frame_bgr = draw_viewfinder_overlay(
            raw_frame_bgr,
            detected_faces,
            tag_prefix="SUBJ",
            draw_crosshairs=True,
        )
    elif selected_mode == "REDACTION_MASK":
        processed_frame_bgr = apply_redaction_mask(
            raw_frame_bgr,
            detected_faces,
            mosaic_block_size=mosaic_size,
        )
    elif selected_mode == "HIGH_CONTRAST_MONO":
        processed_frame_bgr = apply_high_contrast_mono(
            raw_frame_bgr,
            detected_faces,
            grain_sigma=grain_intensity,
        )
    else:
        processed_frame_bgr = raw_frame_bgr.copy()

    # Convert BGR to RGB for Streamlit canvas display
    viewfinder_rgb = cv2.cvtColor(processed_frame_bgr, cv2.COLOR_BGR2RGB)

    # --- Render Optical Viewfinder Column ---
    with col_viewfinder:
        aspect_ratio_str = f"{frame_w / np.gcd(frame_w, frame_h):.0f}:{frame_h / np.gcd(frame_w, frame_h):.0f}"

        st.markdown(
            f"""
        <div class="viewfinder-card">
            <div class="viewfinder-bar">
                <span>VIEWFINDER // SENSOR_FRAME: {frame_w}x{frame_h} PX</span>
                <span style="color: #FF4F00;">● RETICLE LOCK: {subject_count:02d} DETECTED</span>
                <span>ASPECT RATIO: {aspect_ratio_str}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.image(viewfinder_rgb, use_container_width=True)

        st.markdown(
            f"""
            <div class="viewfinder-bar-subtle">
                <span>OPTICAL ENGINE: HAAR CASCADE</span>
                <span>SPECTRAL FILTER: {selected_mode}</span>
                <span>FIELD SCAN LATENCY: {latency_ms:.2f} MS</span>
                <span>COVERAGE: {spatial_density_pct:.2f}%</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # --- Render Telemetry Ledger Column ---
    with col_telemetry:
        st.markdown('<div class="telemetry-section-title" style="margin-top: 1.25rem;">02 // SPATIAL SPECIFICATIONS</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
        <div class="spec-grid">
            <div class="spec-box">
                <div class="micro-label">SUBJECT COUNT</div>
                <div class="spec-val">{subject_count:02d}</div>
            </div>
            <div class="spec-box">
                <div class="micro-label">FRAME RESOLUTION</div>
                <div class="spec-val-sm">{frame_w} × {frame_h}</div>
            </div>
            <div class="spec-box">
                <div class="micro-label">PROCESSING TIME</div>
                <div class="spec-val">{latency_ms:.1f} <span style="font-size: 11px; font-weight: normal; color: #6C6B66;">MS</span></div>
            </div>
            <div class="spec-box">
                <div class="micro-label">SPATIAL DENSITY</div>
                <div class="spec-val">{spatial_density_pct:.2f} <span style="font-size: 11px; font-weight: normal; color: #6C6B66;">%</span></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="telemetry-section-title">03 // TARGET COORDINATE MATRIX</div>', unsafe_allow_html=True)

        if subject_count > 0:
            table_rows_html = ""
            ledger_records = []

            for i, (x, y, w, h) in enumerate(detected_faces):
                subj_tag = f"SUBJ_{i+1:02d}" if selected_mode != "REDACTION_MASK" else f"REDACTED_{i+1:02d}"
                face_area = w * h
                cov_pct = (face_area / frame_area) * 100.0
                status_label = "LOCKED" if selected_mode != "REDACTION_MASK" else "MASKED"
                status_class = "status-locked" if selected_mode != "REDACTION_MASK" else "status-redacted"

                table_rows_html += f"""
                <tr>
                    <td><span class="tag-badge">{subj_tag}</span></td>
                    <td>{x}, {y}</td>
                    <td>{w}×{h}</td>
                    <td>{face_area:,}</td>
                    <td>{cov_pct:.1f}%</td>
                    <td><span class="{status_class}">{status_label}</span></td>
                </tr>
                """

                ledger_records.append(
                    {
                        "TIMESTAMP_UTC": current_timestamp_utc,
                        "SUBJECT_ID": subj_tag,
                        "ORIGIN_X_PX": int(x),
                        "ORIGIN_Y_PX": int(y),
                        "WIDTH_PX": int(w),
                        "HEIGHT_PX": int(h),
                        "AREA_PX2": int(face_area),
                        "FRAME_WIDTH_PX": int(frame_w),
                        "FRAME_HEIGHT_PX": int(frame_h),
                        "SPATIAL_COVERAGE_PCT": round(cov_pct, 3),
                        "PIPELINE_MODE": selected_mode,
                        "PROCESSING_TIME_MS": round(latency_ms, 2),
                    }
                )

            st.markdown(
                f"""
            <table class="ledger-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>ORIGIN (X,Y)</th>
                        <th>DIM (W×H)</th>
                        <th>AREA</th>
                        <th>DENS</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
            """,
                unsafe_allow_html=True,
            )

            # Exportable Field Log Section
            st.markdown('<div class="telemetry-section-title">04 // EXPORT FIELD LOGS</div>', unsafe_allow_html=True)

            # 1. Processed Optical Frame Export
            success_encode, encoded_png = cv2.imencode(".png", processed_frame_bgr)
            if success_encode:
                st.download_button(
                    label="DOWNLOAD OPTICAL FRAME [.PNG]",
                    data=encoded_png.tobytes(),
                    file_name=f"optics_capture_{selected_mode.lower()}_{int(time.time())}.png",
                    mime="image/png",
                )

            # 2. Telemetry Ledger CSV Export
            df_ledger = pd.DataFrame(ledger_records)
            csv_buffer = io.StringIO()
            df_ledger.to_csv(csv_buffer, index=False)

            st.download_button(
                label="DOWNLOAD TELEMETRY LEDGER [.CSV]",
                data=csv_buffer.getvalue(),
                file_name=f"telemetry_ledger_{int(time.time())}.csv",
                mime="text/csv",
            )

        else:
            st.markdown(
                """
            <div class="callout-box callout-box-alert">
                NO SUBJECTS DETECTED IN OPTICAL FIELD.<br>
                ADJUST SENSITIVITY CALIBRATION (REDUCE SCALE FACTOR OR MINIMUM NEIGHBORS) OR REPOSITION TARGET.
            </div>
            """,
                unsafe_allow_html=True,
            )

else:
    # Awaiting input stream
    with col_viewfinder:
        st.markdown(
            """
        <div class="viewfinder-card">
            <div class="viewfinder-bar">
                <span>VIEWFINDER // SENSOR_FRAME: STANDBY</span>
                <span style="color: #6C6B66;">NO SIGNAL</span>
                <span>ASPECT RATIO: --</span>
            </div>
            <div style="padding: 4rem 2rem; text-align: center; background-color: #EAE8E2;">
                <div class="micro-label" style="font-size: 13px; margin-bottom: 8px;">OPTICAL SENSOR STREAM OFFLINE</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #6C6B66;">
                    SELECT BENCHMARK PORTRAIT OR ACTIVATE INPUT SENSOR (IMAGE UPLOAD / WEBCAM)
                </div>
            </div>
            <div class="viewfinder-bar-subtle">
                <span>OPTICAL ENGINE: READY</span>
                <span>SPECTRAL FILTER: STANDBY</span>
                <span>FIELD SCAN LATENCY: 0.00 MS</span>
                <span>COVERAGE: 0.00%</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_telemetry:
        st.markdown('<div class="telemetry-section-title" style="margin-top: 1.25rem;">02 // SPATIAL SPECIFICATIONS</div>', unsafe_allow_html=True)
        st.markdown(
            """
        <div class="spec-grid">
            <div class="spec-box">
                <div class="micro-label">SUBJECT COUNT</div>
                <div class="spec-val">00</div>
            </div>
            <div class="spec-box">
                <div class="micro-label">FRAME RESOLUTION</div>
                <div class="spec-val-sm">-- × --</div>
            </div>
            <div class="spec-box">
                <div class="micro-label">PROCESSING TIME</div>
                <div class="spec-val">0.0 <span style="font-size: 11px; font-weight: normal; color: #6C6B66;">MS</span></div>
            </div>
            <div class="spec-box">
                <div class="micro-label">SPATIAL DENSITY</div>
                <div class="spec-val">0.00 <span style="font-size: 11px; font-weight: normal; color: #6C6B66;">%</span></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="callout-box">
            AWAITING OPTICAL FRAME STREAM.<br>
            INITIALIZE SENSOR CAPTURE VIA BENCHMARK OR LOCAL CAMERA INPUT TO POPULATE TELEMETRY MATRIX.
        </div>
        """,
            unsafe_allow_html=True,
        )

