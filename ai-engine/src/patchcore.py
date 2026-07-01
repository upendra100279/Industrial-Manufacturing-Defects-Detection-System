"""
Lightweight PatchCore-style anomaly detector for the "Advanced Feature".

Unlike YOLO (supervised, needs labeled defects per class), PatchCore is
trained ONLY on "good" images. At inference, it scores how far a test
image's deep features are from the "normal" feature memory bank —
producing an anomaly score AND a pixel-level heatmap, with zero need for
defect annotations. This is the standard approach used on MVTec AD's
official benchmark.

Simplified implementation: ResNet feature extractor + k-NN distance to
a coreset memory bank of normal-image patch features.
"""
import torch
import torchvision.models as models
import torchvision.transforms as T
import numpy as np
import cv2
from sklearn.neighbors import NearestNeighbors


class PatchCore:
    def __init__(self, device: str = "cpu", backbone_layer: str = "layer2"):
        self.device = device
        resnet = models.wide_resnet50_2(weights=models.Wide_ResNet50_2_Weights.IMAGENET1K_V1)
        resnet.eval().to(device)

        self.features = {}
        getattr(resnet, backbone_layer).register_forward_hook(self._hook("feat"))
        self.backbone = resnet

        self.transform = T.Compose([
            T.ToPILImage(),
            T.Resize((256, 256)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        self.memory_bank: np.ndarray | None = None
        self.knn: NearestNeighbors | None = None

    def _hook(self, name):
        def fn(_, __, output):
            self.features[name] = output
        return fn

    @torch.no_grad()
    def _extract_patch_features(self, image_bgr: np.ndarray):
        img_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)
        self.backbone(tensor)
        feat_map = self.features["feat"]  # (1, C, H, W)
        b, c, h, w = feat_map.shape
        patches = feat_map.permute(0, 2, 3, 1).reshape(h * w, c)
        return patches.cpu().numpy(), (h, w)

    def fit(self, good_image_paths: list[str], coreset_ratio: float = 0.1):
        """Builds the normal-feature memory bank from defect-free images."""
        all_patches = []
        for path in good_image_paths:
            img = cv2.imread(path)
            patches, _ = self._extract_patch_features(img)
            all_patches.append(patches)

        all_patches = np.concatenate(all_patches, axis=0)

        n_keep = max(1, int(len(all_patches) * coreset_ratio))
        idx = np.random.choice(len(all_patches), n_keep, replace=False)
        self.memory_bank = all_patches[idx]

        self.knn = NearestNeighbors(n_neighbors=1).fit(self.memory_bank)
        print(f"PatchCore memory bank built: {len(self.memory_bank)} patch features "
              f"from {len(good_image_paths)} normal images")

    def score(self, image_bgr: np.ndarray):
        """
        Returns (anomaly_score, heatmap) where heatmap is a (H,W) float
        array of per-patch anomaly distances, resized to the input image.
        """
        if self.knn is None:
            raise RuntimeError("Call fit() before score() — no memory bank loaded")

        patches, (h, w) = self._extract_patch_features(image_bgr)
        distances, _ = self.knn.kneighbors(patches)
        distances = distances.reshape(h, w)

        anomaly_score = float(distances.max())
        heatmap = cv2.resize(distances, (image_bgr.shape[1], image_bgr.shape[0]))
        heatmap_norm = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)

        return anomaly_score, heatmap_norm

    def save(self, path: str):
        np.save(path, self.memory_bank)

    def load(self, path: str):
        self.memory_bank = np.load(path)
        self.knn = NearestNeighbors(n_neighbors=1).fit(self.memory_bank)
