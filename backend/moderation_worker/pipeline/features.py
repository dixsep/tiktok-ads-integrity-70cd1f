"""Extract a flat feature dict from a raw ad row."""
import re
from urllib.parse import urlparse

_PUNCT_RUN = re.compile(r"[!?]{3,}")


def extract_features(ad: dict) -> dict:
    text = f"{ad['headline']} {ad['body']}".lower()
    creative_host = urlparse(ad["creative_url"]).hostname or ""
    return {
        "text": text,
        "char_count": len(text),
        "exclaim_runs": len(_PUNCT_RUN.findall(text)),
        "upper_ratio": _upper_ratio(f"{ad['headline']} {ad['body']}"),
        "landing_domain": ad["landing_domain"].lower(),
        "creative_host": creative_host.lower(),
    }


def _upper_ratio(s: str) -> float:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    return sum(c.isupper() for c in letters) / len(letters)
