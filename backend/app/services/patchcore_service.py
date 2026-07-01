"""
Optional anomaly-detection service wrapper around the PatchCore module
in ai-engine/src/patchcore.py. Not wired into a route by default —
import and call fit()/score() if you want to add an /api/detect/anomaly
endpoint. Kept separate from yolo_service since it has a different
lifecycle (must be fit on "good" images before it can score anything).
"""
import sys
import os

# Allow importing the ai-engine package from the backend without packaging it
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../ai-engine/src"))

try:
    from patchcore import PatchCore  # noqa: E402
except ImportError:
    PatchCore = None


class PatchCoreService:
    def __init__(self):
        self.model = PatchCore() if PatchCore else None
        self.is_fitted = False

    def fit(self, good_image_paths: list[str]):
        if self.model is None:
            raise RuntimeError("PatchCore module not available")
        self.model.fit(good_image_paths)
        self.is_fitted = True

    def score(self, image_bgr):
        if not self.is_fitted:
            raise RuntimeError("Call fit() with normal images before scoring")
        return self.model.score(image_bgr)


patchcore_service = PatchCoreService()
