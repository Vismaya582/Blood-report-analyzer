import pdfplumber
import re

def extract_biological_data(pdf_path):
    data = {
        "patient_info": {},
        "results": {}
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")

            for line in lines:
                line = line.strip()
                age_match = re.search(r"Age\s*:\s*(\d+)", line, re.IGNORECASE)
                if age_match:
                    data["patient_info"]["age"] = int(age_match.group(1))

                gender_match = re.search(r"(?:Sex|Gender)\s*:\s*(Male|Female|Other)", line, re.IGNORECASE)
                if gender_match:
                    data["patient_info"]["gender"] = gender_match.group(1).capitalize()

                match = re.match(
                    r"([A-Za-z0-9 ()/\-+]+?)\s+([\d.]+)\s*(?:High|Low|Borderline)?\s*(?:[\d.\-\u2013> <]+)?\s+([a-zA-Z/%\u03bcgFLdLpg]+)",
                    line
                )
                if match:
                    term = match.group(1).strip()
                    value = match.group(2).strip()
                    unit = match.group(3).strip()
                    data["results"][term] = f"{value} {unit}"

    flat_data = {**data["patient_info"]}
    flat_data.update(data["results"])
    return flat_data
