import os
import json
import time

from dotenv import load_dotenv
from google import genai
from PIL import Image

try:
    from src.image_validator import validate_image
except ModuleNotFoundError:
    from image_validator import validate_image


load_dotenv()


def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def fallback_selection(
    food_item,
    image_paths
):

    if not image_paths:
        return None

    best_path = None
    best_score = -1
    best_data = None

    for image_path in image_paths:

        try:

            data = validate_image(
                image_path
            )

            if not os.path.exists(
                image_path
            ):
                continue

            score = 0

            width = data.get(
                "width",
                0
            )

            height = data.get(
                "height",
                0
            )

            blur = data.get(
                "blur_score",
                0
            )

            size = data.get(
                "file_size_mb",
                0
            )

            issues = data.get(
                "issues",
                []
            )

            # Resolution score
            if width >= 1200:
                score += 25
            elif width >= 800:
                score += 15

            if height >= 800:
                score += 25
            elif height >= 600:
                score += 15

            # Sharpness score
            if blur >= 500:
                score += 30
            elif blur >= 250:
                score += 20
            elif blur >= 100:
                score += 10

            # Aspect ratio
            if height > 0:

                ratio = width / height

                if 1.2 <= ratio <= 1.8:
                    score += 10

                elif 0.8 <= ratio <= 2.0:
                    score += 5

            # File size
            if 0 < size <= 5:
                score += 10

            # Penalize problems
            score -= len(issues) * 10

            if score > best_score:

                best_score = score
                best_path = image_path
                best_data = data

        except Exception as e:

            print(
                f"Fallback validation failed for "
                f"{image_path}: {e}"
            )

    if not best_path:

        return None

    confidence = max(
        50,
        min(
            best_score,
            90
        )
    )

    return {
        "best_image": image_paths.index(
            best_path
        ) + 1,
        "best_path": best_path,
        "confidence": confidence,
        "reason": (
            "Gemini was unavailable, so the image "
            "was selected using automatic image-quality "
            "validation based on resolution, sharpness, "
            "aspect ratio, and file size."
        ),
        "method": "fallback"
    }


def select_best_image(
    food_item,
    image_paths
):

    if not image_paths:
        return None

    client = get_gemini_client()

    if client is None:

        print(
            "Gemini API key not available."
        )

        print(
            "Using automatic fallback selection."
        )

        return fallback_selection(
            food_item,
            image_paths
        )

    prompt = f"""
You are an AI food image selection agent.

Food item:
{food_item}

You will receive multiple candidate images.

Evaluate every image and select the image that best represents
the requested food item.

Consider:

1. Does the image actually show the requested food?
2. Is the food clearly visible?
3. Is the main dish reasonably centered?
4. Is it suitable for a restaurant or food menu?
5. Is the dish not excessively cropped?
6. Is the image reasonably sharp and clear?
7. Does the image look natural and relevant?
8. Avoid large text, advertisements, watermarks,
   logos, or unrelated objects.

Return ONLY valid JSON:

{{
    "best_image": 1,
    "confidence": 95,
    "reason": "Short explanation."
}}

Rules:

- best_image must be the candidate number.
- confidence must be an integer from 0 to 100.
- reason must briefly explain the selection.
- Do not return Markdown.
- Do not return anything outside the JSON object.
"""

    contents = [prompt]

    opened_images = []

    for i, image_path in enumerate(
        image_paths,
        start=1
    ):

        try:

            image = Image.open(
                image_path
            )

            image.load()

            opened_images.append(
                image
            )

            contents.append(
                f"Candidate Image {i}"
            )

            contents.append(
                image
            )

        except Exception as e:

            print(
                f"Could not open candidate "
                f"{i}: {e}"
            )

    if not opened_images:

        return None

    # Try Gemini
    for attempt in range(3):

        try:

            print(
                f"Gemini attempt "
                f"{attempt + 1}/3..."
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents
            )

            text = response.text

            if not text:

                raise ValueError(
                    "Gemini returned an empty response."
                )

            text = text.strip()

            # Remove Markdown code fences if returned
            if text.startswith("```"):

                text = text.replace(
                    "```json",
                    ""
                )

                text = text.replace(
                    "```JSON",
                    ""
                )

                text = text.replace(
                    "```",
                    ""
                )

                text = text.strip()

            result = json.loads(
                text
            )

            best_number = int(
                result["best_image"]
            )

            if (
                best_number < 1
                or best_number > len(image_paths)
            ):

                raise ValueError(
                    "Gemini returned an invalid image number."
                )

            try:

                confidence = int(
                    result.get(
                        "confidence",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                confidence = 0

            confidence = max(
                0,
                min(
                    confidence,
                    100
                )
            )

            reason = str(
                result.get(
                    "reason",
                    ""
                )
            ).strip()

            print(
                "Gemini successfully selected an image."
            )

            return {
                "best_image": best_number,
                "best_path": image_paths[
                    best_number - 1
                ],
                "confidence": confidence,
                "reason": reason,
                "method": "gemini"
            }

        except Exception as e:

            error_text = str(e)

            print(
                f"Gemini attempt "
                f"{attempt + 1} failed:"
            )

            print(
                error_text
            )

            # Quota/rate-limit errors should
            # immediately use fallback.
            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED"
                in error_text
                or "quota" in error_text.lower()
                or "rate limit"
                in error_text.lower()
            ):

                print(
                    "\nGemini quota/rate limit "
                    "detected."
                )

                print(
                    "Switching to automatic "
                    "fallback selection."
                )

                return fallback_selection(
                    food_item,
                    image_paths
                )

            # Retry temporary errors
            if attempt < 2:

                wait_time = 5 * (
                    attempt + 1
                )

                print(
                    f"Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(
                    wait_time
                )

    # If Gemini completely fails,
    # continue with fallback.
    print(
        "\nGemini failed after all attempts."
    )

    print(
        "Using automatic fallback selection."
    )

    return fallback_selection(
        food_item,
        image_paths
    )