# PyTorch Pre-trained Model Checkpoint
> **File:** `emergency_vision_backbone_weights.pt` (~100 MB)  
> **Architecture:** ResNet-50 / TraumaNet Vision Backbone  
> **Format:** PyTorch Checkpoint State Dict

### Overview
This checkpoint contains the pre-trained feature extraction backbone weights used for:
- Deep convolutional feature embeddings for trauma tissue classification
- Multiscale erythema and contour feature maps
- Edge gradient boundary estimation for lacerations and bone dislocations

These weights integrate with the OpenCV visual pipeline to enable deterministic offline inference.
