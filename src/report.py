import os

import pandas as pd


def generate_report(
    results,
    output_file="logs/processing_report.xlsx"
):

    os.makedirs(
        "logs",
        exist_ok=True
    )

    report_data = []

    for result in results:

        report_data.append(
            {
                "Food Item": result.get(
                    "food_item",
                    ""
                ),

                "Status": (
                    "Success"
                    if result.get("success")
                    else "Failed"
                ),

                "Selected Image": result.get(
                    "selected_image",
                    ""
                ),

                "AI Confidence": result.get(
                    "confidence",
                    ""
                ),

                "AI Reason": result.get(
                    "reason",
                    ""
                ),

                "Final Image": result.get(
                    "processed_path",
                    ""
                ),

                "Width": result.get(
                    "width",
                    ""
                ),

                "Height": result.get(
                    "height",
                    ""
                ),

                "Size (MB)": result.get(
                    "size_mb",
                    ""
                ),

                "Google Drive URL": result.get(
                    "drive_url",
                    ""
                ),

                "Error": result.get(
                    "error",
                    ""
                )
            }
        )

    df = pd.DataFrame(
        report_data
    )

    df.to_excel(
        output_file,
        index=False
    )

    return output_file