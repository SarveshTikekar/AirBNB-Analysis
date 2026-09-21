import json
import re
import shutil
import time
import unicodedata
from pathlib import Path

import ollama


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
LISTINGS_DIR = BASE_DIR / "Datasets" / "Listings"

MODEL_NAME = "qwen2.5:3b"
OLLAMA_HOST = "http://localhost:11434"

CONTEXT_SIZE = 4096
NUM_PREDICT = 220
KEEP_ALIVE = "30m"

client = ollama.Client(host=OLLAMA_HOST)


# ============================================================
# PROMPT
# ============================================================

SYSTEM_PROMPT = """You are an expert Airbnb listing editor.

Rewrite the supplied Airbnb property description into a concise,
polished listing opener suitable for a professional dashboard.

STRICT RULES:

1. Use English only.
3. Use ONLY facts explicitly stated in the source.
4. Never guess, estimate, assume, or infer information.
5. Never invent guest capacity, amenities, facilities, or rules.
6. Prioritize:
   - Property type
   - Explicit guest capacity
   - Location/accessibility
   - Important amenities
   - Important restrictions
7. Remove:
   - Personal stories
   - Guest reviews
   - Host introductions
   - Registration numbers
   - Pandemic/COVID information
   - Excessive marketing language
   - Repetition
   - Irrelevant details
8. Preserve important factual details such as locations,
   distances, amenities, restrictions, and stated capacity.
9. Write complete, grammatically correct English sentences.
10. Fix spelling, grammar, punctuation, capitalization,
    and awkward sentence structure.
11. Remove emojis and decorative/special characters.
12. Keep the writing natural, professional, concise, and inviting.
13. Do not add headings, labels, bullet points, commentary,
    or explanations.
14. Return ONLY the final listing description.
"""


def get_length_instruction(word_count):
    if word_count < 128:
        return (
            "The source is under 128 words. Clean it without intentionally "
            "expanding it, and keep the final description under 128 words."
        )

    return (
        "The source is at least 128 words. Refine the final description to "
        "between 128 and 160 words, inclusive."
    )


# ============================================================
# VALIDATION
# ============================================================

def is_invalid_description(text):
    if text is None:
        return True

    return str(text).strip() in (
        "",
        "No Description Available"
    )


def validate_output(output, word_count):
    if not output:
        return False

    output = output.strip()

    output_word_count = len(output.split())

    if word_count < 128 and output_word_count >= 128:
        return False

    if word_count >= 128 and not 128 <= output_word_count <= 160:
        return False

    # Minimum useful output
    if len(output) < 20:
        return False

    # Must end as a complete piece of writing
    if not output.endswith((".", "!", "?")):
        return False

    return True


# ============================================================
# PREPROCESSING
# ============================================================

def preprocess_description(text):
    text = str(text)

    # HTML line breaks -> spaces
    text = re.sub(
        r"<br\s*/?>",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Remove remaining HTML tags
    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    # Normalize Unicode
    text = unicodedata.normalize(
        "NFKC",
        text
    )

    # Remove emojis and non-English scripts
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove spaces before punctuation
    text = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        text
    )

    return text.strip()


# ============================================================
# OLLAMA
# ============================================================

def clean_description(text):

    if is_invalid_description(text):
        return ""

    processed = preprocess_description(text)

    if not processed:
        return ""

    word_count = len(processed.split())
    prompt = f"{SYSTEM_PROMPT}\n\nLENGTH REQUIREMENT:\n{get_length_instruction(word_count)}"

    try:

        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": processed
                }
            ],
            options={
                "temperature": 0.0,
                "num_predict": NUM_PREDICT,
                "num_ctx": CONTEXT_SIZE
            },
            keep_alive=KEEP_ALIVE
        )

        output = response["message"]["content"].strip()

        if validate_output(output, word_count):
            return output

        return None

    except Exception as e:

        print(f"\nERROR: {e}")

        return None


# ============================================================
# JSON
# ============================================================

def add_cleaned_description(record, cleaned):

    new_record = {}

    for key, value in record.items():

        # Replace existing cleaned_description
        if key == "cleaned_description":
            new_record[key] = cleaned
            continue

        new_record[key] = value

        # Insert immediately after description
        if key == "description":
            new_record["cleaned_description"] = cleaned

    # Safety fallback
    if "cleaned_description" not in new_record:
        new_record["cleaned_description"] = cleaned

    return new_record


def save_json(path, records):

    temp_path = path.with_suffix(".tmp")

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as f:

        for record in records:

            json.dump(
                record,
                f,
                ensure_ascii=False,
                separators=(",", ":")
            )

            f.write("\n")

    # Atomic replacement
    temp_path.replace(path)


# ============================================================
# PROCESS FILE
# ============================================================

def process_file(path):

    print(f"\nProcessing: {path.name}")

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        records = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    total = len(records)

    # Backup original only once
    backup_path = path.with_suffix(".json.bak")

    if not backup_path.exists():
        shutil.copy2(path, backup_path)

    start = time.perf_counter()

    processed = 0
    skipped = 0
    rejected = 0

    for index, record in enumerate(records, 1):

        description = record.get("description")

        # Missing / unavailable description
        if is_invalid_description(description):

            records[index - 1] = add_cleaned_description(
                record,
                ""
            )

            skipped += 1

            save_json(
                path,
                records
            )

            continue

        # Always regenerate
        cleaned = clean_description(description)

        if cleaned is None:

            rejected += 1

        else:

            # Always overwrite previous generation
            records[index - 1] = add_cleaned_description(
                record,
                cleaned
            )

            processed += 1

            # Save immediately
            save_json(
                path,
                records
            )

        elapsed = time.perf_counter() - start

        rate = (
            processed / elapsed * 60
            if processed
            else 0
        )

        remaining = total - index

        eta = (
            remaining / (processed / elapsed) / 60
            if processed
            else 0
        )

        print(
            f"\r  {index:,}/{total:,} "
            f"({index / total * 100:5.1f}%) "
            f"| {rate:5.1f}/min "
            f"| ETA {eta:5.1f} min",
            end="",
            flush=True
        )

    elapsed = time.perf_counter() - start

    print(
        f"\n  Done | "
        f"Generated: {processed:,} | "
        f"Skipped: {skipped:,} | "
        f"Rejected: {rejected:,} | "
        f"{elapsed / 60:.1f} min"
    )

    return processed


# ============================================================
# MAIN
# ============================================================

def main():

    print("Airbnb Description Cleaner")
    print(f"Model: {MODEL_NAME}")
    print(f"Context: {CONTEXT_SIZE}")
    print("Mode: Sequential")
    print("Pipeline: Single-pass cleaning + editing")
    print("Regeneration: ON")

    files = sorted(
        LISTINGS_DIR.glob("*_Listings.json")
    )

    if not files:

        print("No listing JSON files found.")
        return

    total_processed = 0

    for path in files:

        total_processed += process_file(path)

    print(
        f"\nComplete. "
        f"Descriptions generated: {total_processed:,}"
    )


if __name__ == "__main__":
    main()
