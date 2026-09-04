from pathlib import Path

import numpy as np
import pandas as pd
import torch

from PIL import Image

from torchvision.models import (
    mobilenet_v3_small,
    MobileNet_V3_Small_Weights
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

IMAGE_DIR = DATA_DIR / "Jewelry Images"

CSV_PATH = DATA_DIR / "candidate_dataset.csv"


# ============================================================
# 2. LOAD LIGHTWEIGHT IMAGE MODEL
# ============================================================

print("\nLoading lightweight image model...")

device = "cpu"

print(f"Device: {device}")


# Use pretrained MobileNetV3-Small
weights = MobileNet_V3_Small_Weights.DEFAULT

model = mobilenet_v3_small(
    weights=weights
)


# Remove the final classification layer.
# The remaining network produces visual features.
model.classifier = torch.nn.Identity()

model.to(device)

model.eval()


# Image preprocessing
preprocess = weights.transforms()


print("MobileNetV3-Small model loaded successfully.")


# ============================================================
# 3. IMAGE EMBEDDING FUNCTION
# ============================================================

def get_image_embedding(image):

    """
    Convert an image into a normalized
    visual embedding.
    """

    # Make sure image is RGB
    image = image.convert("RGB")


    # --------------------------------------------------------
    # Prepare image
    # --------------------------------------------------------

    image_tensor = preprocess(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    # Move to CPU
    image_tensor = image_tensor.to(device)


    # --------------------------------------------------------
    # Generate visual features
    # --------------------------------------------------------

    with torch.no_grad():

        features = model(image_tensor)


    # --------------------------------------------------------
    # Convert to NumPy
    # --------------------------------------------------------

    embedding = (
        features
        .cpu()
        .numpy()[0]
    )


    # --------------------------------------------------------
    # L2 normalize
    # --------------------------------------------------------

    embedding = embedding / (
        np.linalg.norm(embedding)
        + 1e-12
    )


    return embedding


# ============================================================
# 4. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(
    CSV_PATH
)


print(
    f"Total products: {len(df)}"
)


print("\nProduct counts:")

print(
    df["product_type"].value_counts()
)


# ============================================================
# 5. FILTER EARRINGS
# ============================================================

earrings_df = df[
    df["product_type"]
    .str.lower()
    == "earrings"
].copy()


print(
    f"\nEarrings available for matching: "
    f"{len(earrings_df)}"
)


# ============================================================
# 6. PRECOMPUTE EARRING EMBEDDINGS
# ============================================================

print(
    "\nCreating earring embeddings..."
)


earring_embeddings = []


for _, row in earrings_df.iterrows():

    image_path = (
        IMAGE_DIR /
        row["image_file"]
    )


    # --------------------------------------------------------
    # Check image exists
    # --------------------------------------------------------

    if not image_path.exists():

        print(
            f"WARNING: Image not found: "
            f"{image_path}"
        )

        continue


    print(
        f"Processing "
        f"{row['id']} -> "
        f"{row['image_file']}"
    )


    # --------------------------------------------------------
    # Load image
    # --------------------------------------------------------

    image = Image.open(
        image_path
    ).convert("RGB")


    # --------------------------------------------------------
    # Generate embedding
    # --------------------------------------------------------

    embedding = get_image_embedding(
        image
    )


    # --------------------------------------------------------
    # Store product information
    # --------------------------------------------------------

    earring_embeddings.append(
        {
            "id":
                row["id"],

            "product_type":
                row["product_type"],

            "image_file":
                row["image_file"],

            "embedding":
                embedding
        }
    )


print(
    f"\nCreated embeddings for "
    f"{len(earring_embeddings)} earrings."
)


# ============================================================
# 7. FIND MATCHES
# ============================================================

def find_matches(
    necklace_image,
    top_k=3
):

    """
    Compare the uploaded necklace
    against all inventory earrings.
    """


    # --------------------------------------------------------
    # Generate necklace embedding
    # --------------------------------------------------------

    necklace_embedding = (
        get_image_embedding(
            necklace_image
        )
    )


    # --------------------------------------------------------
    # Compare against earrings
    # --------------------------------------------------------

    results = []


    for item in earring_embeddings:

        earring_embedding = (
            item["embedding"]
        )


        # ----------------------------------------------------
        # Cosine similarity
        #
        # Both embeddings are normalized,
        # so dot product = cosine similarity.
        # ----------------------------------------------------

        similarity = float(
            np.dot(
                necklace_embedding,
                earring_embedding
            )
        )


        results.append(
            {
                "id":
                    item["id"],

                "product_type":
                    item["product_type"],

                "image_file":
                    item["image_file"],

                "similarity":
                    similarity
            }
        )


    # --------------------------------------------------------
    # Highest similarity first
    # --------------------------------------------------------

    results.sort(
        key=lambda item:
            item["similarity"],
        reverse=True
    )


    # --------------------------------------------------------
    # Return Top K
    # --------------------------------------------------------

    return results[:top_k]


# ============================================================
# 8. TEST THE MATCHING ENGINE
# ============================================================

if __name__ == "__main__":

    print(
        "\n===================================="
    )

    print(
        "TESTING JEWELLERY MATCHING SYSTEM"
    )

    print(
        "===================================="
    )


    # --------------------------------------------------------
    # Test necklace
    # --------------------------------------------------------

    test_image_path = (
        IMAGE_DIR /
        "Nck_1.jpg"
    )


    # --------------------------------------------------------
    # Check necklace exists
    # --------------------------------------------------------

    if not test_image_path.exists():

        print(
            "\nERROR:"
        )

        print(
            f"Necklace image not found:"
            f"\n{test_image_path}"
        )

        raise SystemExit


    print(
        f"\nTesting necklace:"
        f"\n{test_image_path}"
    )


    # --------------------------------------------------------
    # Load necklace
    # --------------------------------------------------------

    test_image = Image.open(
        test_image_path
    ).convert("RGB")


    # --------------------------------------------------------
    # Find matches
    # --------------------------------------------------------

    matches = find_matches(
        test_image,
        top_k=3
    )


    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print(
        "\n===================================="
    )

    print(
        "TOP 3 MATCHING EARRINGS"
    )

    print(
        "===================================="
    )


    for index, match in enumerate(
        matches,
        start=1
    ):

        print(
            f"{index}. "
            f"{match['id']} | "
            f"{match['image_file']} | "
            f"Similarity: "
            f"{match['similarity']:.4f}"
        )


    print(
        "\n===================================="
    )

    print(
        "TEST COMPLETED SUCCESSFULLY"
    )

    print(
        "===================================="
    )
