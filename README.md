# 💎 AI Jewellery Matcher

An AI-powered visual recommendation prototype that recommends matching earrings for a selected necklace from a predefined jewellery inventory.

## Problem

Given a necklace image, the system should identify visually similar earrings from the available jewellery inventory.

The assignment provides:

- 5 necklace images
- 15 earring images
- A CSV file containing product IDs, product types and image filenames

## Solution

The system uses a pretrained CLIP vision model to convert jewellery images into visual embeddings.

The workflow is:

1. Load the jewellery inventory from CSV.
2. Filter the inventory to earrings.
3. Generate CLIP embeddings for all 15 earrings.
4. Accept a necklace image as input.
5. Generate a CLIP embedding for the necklace.
6. Calculate cosine similarity between the necklace and every earring.
7. Rank the earrings by similarity.
8. Return the top 3 matching earrings.
9. Display the recommended jewellery images in the web interface.

## Architecture

```text
User
  |
  v
Frontend
HTML + CSS + JavaScript
  |
  | POST /match
  v
FastAPI Backend
  |
  v
CLIP Vision Encoder
  |
  +----------------------+
  |                      |
  v                      v
Necklace Embedding   Earring Embeddings
                       (15 products)
  |                      |
  +----------+-----------+
             |
             v
      Cosine Similarity
             |
             v
       Ranked Top 3
             |
             v
        JSON Response
             |
             v
       Frontend Results

## Technologies & Tools

### AI / Machine Learning

- Python
- PyTorch
- Hugging Face Transformers
- CLIP (`openai/clip-vit-base-patch32`)
- NumPy

### Backend

- FastAPI
- Uvicorn

### Frontend

- HTML
- CSS
- JavaScript

### Data & Image Processing

- Pandas
- Pillow (PIL)

### Development Tools

- Visual Studio Code
- Git
- GitHub

## Dataset

The provided dataset contains:

- 5 necklace images
- 15 earring images
- `candidate_dataset.csv`

The CSV file contains product information such as product IDs, product types, and image filenames.
