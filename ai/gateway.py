from ai.classification.text_classifier import classify_text

def analyze_complaint(description: str, file_urls: list = None) -> dict:
    """
    Unified entry point for AI analysis.
    Future: If file_urls has images, use image_classifier.py
    For now, purely text-based classification with Gemini.
    """
    
    # Check if we should route to multimodal
    # if file_urls and len(file_urls) > 0:
    #     return classify_multimodal(description, file_urls)
        
    return classify_text(description)
