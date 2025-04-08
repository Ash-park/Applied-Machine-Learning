import re
import numpy as np
import joblib
from typing import Tuple
import sklearn.base


def preprocess_message(message: str) -> str:
    """
    Clean and normalize a text message.
    
    Converts to lowercase, strips out non-alphabetic characters,
    and keeps only word tokens.
    
    Args:
        message (str): The raw input message.
    
    Returns:
        str: Cleaned message string.
    """
    words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
    return ' '.join(words)


def score(text: str, model: sklearn.base.BaseEstimator, threshold: float) -> Tuple[bool, float]:
    vec = joblib.load("vectorizer.joblib")
    processed = preprocess_message(text)
    vect_input = vec.transform([processed])

    probability = model.predict_proba(vect_input)[0][1]
    is_positive = probability >= threshold

    return bool(is_positive), float(probability)
