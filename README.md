💎 AI Jewellery Matcher

An AI-powered visual matching prototype that recommends the most visually similar earrings for a selected necklace from the provided jewellery inventory.

🎯 Objective

Given a necklace image as input, the system compares it against the available earrings in the jewellery inventory and returns the top 3 visually matching earrings.

The provided dataset contains:

5 necklace images
15 earring images
candidate_dataset.csv containing product IDs, product types, and image filenames
🧠 Approach Used

I used a pretrained CLIP (Contrastive Language–Image Pre-training) vision model to compare the jewellery images.

Instead of training an AI model from scratch, CLIP is used to extract a visual embedding from each image.

Image Matching Workflow
Necklace Image
      │
      ▼
CLIP Vision Encoder
      │
      ▼
Necklace Image Embedding
      │
      │
      │     Compare
      │       with
      ▼
15 Earring Embeddings
      │
      ▼
Cosine Similarity
      │
      ▼
Rank by Similarity
      │
      ▼
Top 3 Matching Earrings
Step-by-step
The jewellery inventory is loaded from candidate_dataset.csv.
Products with product_type = Earrings are selected.
CLIP generates an image embedding for each of the 15 earrings.
When a necklace image is selected or uploaded, CLIP generates an embedding for the necklace.
The necklace embedding is compared with every earring embedding.
Cosine similarity is used to measure visual similarity.
The earrings are sorted from highest to lowest similarity.
The top 3 results are returned through the API and displayed in the frontend.

Because the embeddings are normalized, the dot product can be used to calculate cosine similarity efficiently.

Note: The similarity score represents visual embedding similarity and is not a prediction probability or confidence score.

🛠️ Technologies & Tools Used
Backend
Python – Core programming language
FastAPI – REST API for image matching
Uvicorn – ASGI server for running the FastAPI application
AI / Computer Vision
OpenAI CLIP (clip-vit-base-patch32) – Pretrained image representation model
Hugging Face Transformers – Loading and using the CLIP model
PyTorch – Deep learning framework used by CLIP
Image & Data Processing
Pillow (PIL) – Image loading and processing
NumPy – Embedding normalization and cosine similarity calculation
Pandas – Reading and filtering the CSV inventory
Frontend
HTML – Page structure
CSS – Responsive jewellery-themed interface
JavaScript – Image selection, API requests and displaying recommendations
Development Tools
Visual Studio Code
Python Virtual Environment
Git / GitHub
📁 Project Structure
jewlerymatcher/
│
├── data/
│   ├── candidate_dataset.csv
│   │
│   └── Jewelry Images/
│       ├── Nck_1.jpg
│       ├── Nck_2.jpg
│       ├── Nck_3.jpg
│       ├── Nck_4.jpg
│       ├── Nck_5.jpg
│       ├── Ear_1.jpg
│       ├── Ear_2.jpg
│       ├── ...
│       └── Ear_15.jpg
│
├── static/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── app.py
├── matcher.py
├── requirements.txt
├── README.md
└── .gitignore
🚀 How to Run
1. Create a virtual environment
python -m venv venv
2. Activate the virtual environment

Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Start the FastAPI server
uvicorn app:app --reload
5. Open the application
http://127.0.0.1:8000

The API documentation is available at:

http://127.0.0.1:8000/docs
🔌 API
POST /match

Accepts a jewellery image and returns the top matching earrings from the provided inventory.

Example response:

{
  "success": true,
  "matches": [
    {
      "id": "E01",
      "product_type": "Earrings",
      "image_file": "Ear_1.jpg",
      "similarity": 0.91
    },
    {
      "id": "E08",
      "product_type": "Earrings",
      "image_file": "Ear_8.jpg",
      "similarity": 0.87
    },
    {
      "id": "E15",
      "product_type": "Earrings",
      "image_file": "Ear_15.jpg",
      "similarity": 0.84
    }
  ]
}
💡 Why This Approach?

The provided dataset is very small, with only 5 necklaces and 15 earrings, so training a deep learning model from scratch would not be appropriate.

Using a pretrained CLIP model allows the prototype to leverage learned visual representations without requiring model training. The approach is also simple to implement, fast to prototype, and can be extended to a much larger jewellery catalogue.

For a larger production system, the precomputed earring embeddings could be stored in a vector database or an indexing system such as FAISS for faster retrieval.

⚠️ Limitations
The current inventory contains only 15 earrings.
The system primarily measures visual similarity.
Similarity can be affected by image background, lighting, camera angle and composition.
Visual similarity does not necessarily mean that two jewellery pieces are a perfect style or design match.
🔮 Future Improvements

The prototype could be improved by adding:

Jewellery colour detection
Gold/silver/material classification
Shape and design feature extraction
Traditional/modern/bridal style classification
Jewellery-specific fine-tuning
FAISS/vector database for larger inventories
Metadata-aware ranking
User preference-based recommendations
Product catalogue and pricing integration
👨‍💻 Summary

This prototype demonstrates an end-to-end AI visual jewellery recommendation system using a pretrained CLIP model. It accepts a necklace image, generates its visual embedding, compares it against embeddings of the available earrings using cosine similarity, and returns the top 3 visually matching products through a FastAPI backend and web interface.
