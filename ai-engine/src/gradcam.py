"""
Grad-CAM heatmap generation for the YOLO detector — visualizes WHICH
pixels most influenced a given detection, useful for explainability in
the UI ("why did the model flag this region?").

Note: full Grad-CAM on YOLOv8's multi-scale detection head is non-trivial;
this implements a simplified single-target-layer version sufficient for
visual explanation purposes.
"""
import cv2
import numpy as np
import torch


class YOLOGradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate(self, image_tensor: torch.Tensor, class_idx: int) -> np.ndarray:
        self.model.zero_grad()
        output = self.model(image_tensor)

        score = output[0][:, class_idx].max()
        score.backward(retain_graph=True)

        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activations = self.activations.detach()

        for i in range(activations.shape[1]):
            activations[:, i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(activations, dim=1).squeeze().cpu().numpy()
        heatmap = np.maximum(heatmap, 0)
        heatmap = heatmap / (heatmap.max() + 1e-8)
        heatmap = cv2.resize(heatmap, (image_tensor.shape[3], image_tensor.shape[2]))
        return heatmap
