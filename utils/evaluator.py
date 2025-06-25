# utils/evaluator.py
from sklearn.metrics import jaccard_score
import difflib
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from utils.logger import logger


def evaluate_extraction(gpt_data, smol_data):
    logger.info("Inside the evaluator tool...")
    gpt_text = str(gpt_data)
    logger.info("GPT data: %s...", gpt_text[:100])  # Log first 100 chars for brevity
    smol_text = str(smol_data)
    logger.info(f"SmolDocling data: {smol_text[:100]}...")  # Log first 100 chars for brevity

    # Sequence overlap ratio
    sm = difflib.SequenceMatcher(None, gpt_text, smol_text)
    overlap_ratio = sm.ratio()

    # BLEU score
    smoothing = SmoothingFunction().method1
    bleu = sentence_bleu(
        [gpt_text.split()], smol_text.split(), smoothing_function=smoothing
    )

    # Jaccard index (token-level)
    gpt_tokens = set(gpt_text.split())
    smol_tokens = set(smol_text.split())
    intersection = gpt_tokens & smol_tokens
    union = gpt_tokens | smol_tokens
    jaccard = len(intersection) / len(union) if union else 0

    score_summary = {
        "overlap": overlap_ratio,
        "bleu": bleu,
        "jaccard": jaccard
    }

    passed = overlap_ratio >= 0.85 and bleu >= 0.5 and jaccard >= 0.5
    return passed, score_summary
# This function evaluates the extraction quality by comparing GPT and SmolDocling outputs.
# It calculates overlap ratio, BLEU score, and Jaccard index, returning a pass/fail status and a summary of scores.