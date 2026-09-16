# AI Food Image Agent

An automated AI-powered food image processing agent that reads food item names from Excel, searches for relevant food images, validates image quality, uses AI-assisted image selection, processes the selected image, uploads it to Google Drive, and generates a processing report.

---

## Project Overview

The AI Food Image Agent automates the complete workflow of collecting and preparing food images for restaurant/menu applications.

The system minimizes manual image searching and processing by combining:

- Excel data processing
- Google Images search
- Image downloading
- Image quality validation
- AI-based image selection
- Automatic image resizing
- Image compression
- Google Drive upload
- Processing report generation
- Error handling and fallback selection

---

## Workflow

```text
Excel Food Items
       ↓
Read Food Item Names
       ↓
Google Images Search
       ↓
Download Image Candidates
       ↓
Image Quality Validation
       ↓
AI Image Selection
       ↓
Automatic Fallback Selection
       ↓
Resize to 1800 × 1200
       ↓
JPEG Compression
       ↓
Google Drive Upload
       ↓
Processing Report