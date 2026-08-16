import os
import pytest
from ai.duplicate_detection.similarity import cosine_similarity
from ai.duplicate_detection.embeddings import generate_embedding

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Requires GEMINI_API_KEY")
def test_embedding_generation():
    text = "Massive pothole on main road"
    embedding = generate_embedding(text)
    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert isinstance(embedding[0], float)

def test_cosine_similarity():
    # Identical vectors should have similarity 1.0
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert abs(cosine_similarity(v1, v2) - 1.0) < 0.0001
    
    # Orthogonal vectors should have similarity 0.0
    v3 = [0.0, 1.0, 0.0]
    assert abs(cosine_similarity(v1, v3) - 0.0) < 0.0001
    
    # Opposite vectors should have similarity -1.0
    v4 = [-1.0, 0.0, 0.0]
    assert abs(cosine_similarity(v1, v4) - (-1.0)) < 0.0001

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Requires GEMINI_API_KEY")
def test_semantic_similarity_real_world():
    text1 = "Category: POTHOLE. Description: Massive pothole causing accidents near the crossing. Address: Wardha Road"
    text2 = "Category: POTHOLE. Description: Huge crater on the road, cars are getting damaged. Address: Wardha Road"
    text3 = "Category: WATERLOGGING. Description: Severe waterlogging after yesterday's rain. Address: Sitabuldi"
    
    v1 = generate_embedding(text1)
    v2 = generate_embedding(text2)
    v3 = generate_embedding(text3)
    
    sim_1_2 = cosine_similarity(v1, v2)
    sim_1_3 = cosine_similarity(v1, v3)
    
    # The two pothole complaints should be more similar to each other than to the waterlogging one
    assert sim_1_2 > sim_1_3
    
    # Generally, two identical incidents described slightly differently should score high (> 0.75)
    assert sim_1_2 > 0.75
