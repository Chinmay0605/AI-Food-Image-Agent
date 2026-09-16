# 🍽️ AI Food Image Agent

An automated AI-powered food image processing agent that reads food item names from Excel, searches for relevant food images, validates image quality, uses AI to select the most suitable image, processes it into the required format, and uploads the final images to Google Drive.

The system is designed to minimize manual intervention and continue processing other food items even when an individual item encounters an error.

---

## 🚀 Project Overview

The AI Food Image Agent automates the complete food-image preparation workflow:

Excel Food Items
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
Image Processing
        ↓
1800 × 1200 JPG
        ↓
Google Drive Upload
        ↓
Processing Report

The project is suitable for automating restaurant/menu image preparation workflows.

---

## ✨ Features

### 📊 1. Excel Input

The agent reads food item names from an Excel file.

Supported column names:

- `Food Item`
- `item_name`

Duplicate and empty food-item entries are automatically removed.

Example:

| Food Item |
|---|
| Paneer Butter Masala |
| Dal Tadka |
| Veg Biryani |
| Butter Naan |
| Chicken Tikka |

---

### 🔎 2. Automated Image Search

The agent automatically searches Google Images for each food item using SerpApi.

Search queries are generated using the food name along with relevant food/restaurant context.

Multiple candidate images are collected for every food item.

---

### 🖼️ 3. Image Download

Candidate images are automatically downloaded for evaluation.

The system:

- Downloads multiple candidates
- Handles failed downloads
- Uses HTTP timeouts
- Verifies that the downloaded content is an image
- Continues processing when an individual image fails

---

### 🔍 4. Image Quality Validation

Downloaded images are automatically evaluated before AI selection.

Validation checks include:

- Image existence
- Resolution
- File size
- Image readability
- Sharpness / blur detection
- Aspect ratio

OpenCV is used for blur detection using Laplacian variance.

Images with unsuitable properties are removed from the AI-selection candidates.

---

### 🤖 5. AI-Powered Image Selection

Google Gemini is used as the AI image-selection agent.

The AI evaluates candidate images based on factors such as:

- Relevance to the requested food item
- Food visibility
- Dish positioning
- Image clarity
- Restaurant/menu suitability
- Cropping
- Natural appearance
- Unwanted text or advertisements
- Watermarks and logos

The selected image is returned together with a confidence score and explanation.

---

### 🔄 6. Automatic Fallback Selection

If Gemini is temporarily unavailable or reaches an API quota/rate limit, the system does not stop the complete workflow.

Instead, it automatically switches to an image-quality-based fallback selection mechanism.

This allows the agent to continue processing food items even when the AI service is temporarily unavailable.

---

### 🛠️ 7. Image Processing

The selected image is automatically processed into the required output format.

Final specifications:

- Width: **1800 pixels**
- Height: **1200 pixels**
- Format: **JPG**
- Maximum file size: **10 MB**
- RGB color mode
- Automatic quality adjustment when required

Images are center-cropped/fitted while maintaining the required dimensions.

---

### ☁️ 8. Google Drive Upload

Processed images are automatically uploaded to a configured Google Drive folder.

The final files retain the exact food item name.

Example:

```text
Paneer Butter Masala.jpg
Dal Tadka.jpg
Veg Biryani.jpg
Butter Naan.jpg
Chicken Tikka.jpg