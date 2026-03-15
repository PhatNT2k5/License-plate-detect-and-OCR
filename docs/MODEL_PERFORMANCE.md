# Model Performance Details

This document contains detailed performance metrics and training information for the license plate recognition system models.

## Detection Models (Model_DetectorLP)

### Training Summary
- **Architecture**: YOLOv8 variants
- **Task**: License plate detection (bounding box localization)
- **Evaluation Metrics**: mAP50, mAP50-95

### Version Comparison

| Model File | mAP50 | mAP50-95 | Notes |
|------------|-------|----------|-------|
| LP_detect_ver1.pt | 0.99419 | 0.74834 | Baseline version |
| LP_detect_ver2.pt | 0.99487 | 0.75644 | **Best overall performance** |
| LP_detect_ver3.pt | 0.99432 | 0.75507 | High precision |
| LP_detect_ver4.pt | 0.99409 | 0.74047 | Slightly lower recall |
| LP_detect_ver5.pt | 0.99484 | 0.75134 | Consistent performance |

**Analysis**:
- All models show exceptional detection capability (>99.4% mAP50)
- ver2 achieves the best balance of precision and recall
- mAP50-95 scores indicate good performance across different IoU thresholds
- Models are suitable for real-world deployment

## Recognition Models (Model_ReaderLP)

### Training Configuration
- **Model**: YOLO11n (YOLOv11 nano)
- **Framework**: Ultralytics YOLO v8.3.61
- **Environment**: Python 3.10.12, PyTorch 2.5.1+cu121
- **Hardware**: NVIDIA Tesla T4 (15GB VRAM)
- **Dataset Split**: 2,506 training, 682 validation images
- **Image Size**: 640×640 pixels
- **Batch Size**: 16 (detection), variable (recognition)
- **Epochs**: 45 (detection), 30 (recognition)
- **Optimizer**: AdamW (auto-selected)
- **Learning Rate**: 0.00025 (final)
- **Augmentation**: HSV, mosaic, mixup, copy-paste, albumentations

### Character Classes (36 total)
```
0-9: Digits 0 through 9
A-Z: Letters A through Z (excluding O and I to avoid confusion with 0 and 1)
Note: Actual classes include all alphanumeric characters used in Vietnamese license plates
```

### Detailed Performance Metrics

From validation run of best model (45 epochs):

#### Overall Metrics
- **mAP50**: 0.915 (91.5%)
- **mAP50-95**: 0.696 (69.6%)
- **Inference Speed**: ~2.2ms per image
- **Model Size**: ~5.5MB (stripped)

#### Per-Class AP50 Scores
```
0: 0.982    A: 0.866    K: 0.906    U: 0.204
1: 0.978    B: 0.968    L: 0.970    V: 0.930
2: 0.991    C: 0.870    M: 0.792    W: 0.946
3: 0.994    D: 0.487    N: 0.362    X: 0.951
4: 0.992    E: 0.831    O: 0.000    Y: 0.889
5: 0.995    F: 0.995    P: 0.972    Z: 0.839
6: 0.989    G: 0.995    Q: (not shown)
7: 0.994    H: 0.995    R: 0.784
8: 0.994    I: 0.565    S: 0.948
9: 0.947    J: 0.813    T: 0.866
```

#### Key Observations
1. **Excellent Performance**: Digits 0-9 all score >94% AP50
2. **High Confidence Letters**: F, G, H, L, M, P, S, T, V, W, X, Y, Z all >90% AP50
3. **Challenging Characters**:
   - O: 0% (often confused with 0)
   - D: 48.7% (similar to 0/Q)
   - I: 56.5% (similar to 1)
   - J: 81.3% (similar shape variations)
   - N: 36.2% (context-dependent)
   - R: 78.4% (leg variations)

### Training Log Highlights

**Detection Training** (45 epochs):
- Fast convergence: Stable after ~10 epochs
- Minimal overfitting: Validation metrics consistently improve
- Final box_loss: 0.868, cls_loss: 0.425, dfl_loss: 1.004

**Recognition Training** (30 epochs):
- Longer convergence: Steady improvement throughout
- Final box_loss: 0.884, cls_loss: 0.478, dfl_loss: 1.003
- Good generalization: Train/val loss gap minimal

### Recommendations for Production

1. **Detection Model**: Use `LP_detect_ver2.pt` for best overall performance
2. **Recognition Model**: Consider ensemble approach for challenging characters (O, D, I, N, R)
3. **Post-processing**: Apply license plate format validation to correct common confusions:
   - O → 0 in numeric positions
   - I → 1 in numeric positions
   - D → 0/O based on context
4. **Confidence Thresholds**:
   - Detection: >0.5 confidence for reliable boxes
   - Recognition: >0.3 for character classification (adjust per character)

### Reproducing Results

To verify model performance:
```bash
# Detection model validation
yolo val model=models/detection/LP_detect_ver2.pt data=your_data.yaml

# Recognition model validation
yolo val model=models/reader/LP_reader_ver6.pt data=your_char_data.yaml
```

Note: Replace `your_data.yaml` with your dataset configuration file.

### Model Storage and Versioning

Best practices for model management:
- Keep only best performing versions in production
- Archive all training runs for reproducibility
- Use semantic versioning: v1.0.0 (detection), v2.1.0 (recognition)
- Document training data and preprocessing steps
- Validate on hold-out test set before deployment