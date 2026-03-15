# License Plate Recognition System

A computer vision system for automatic license plate detection and recognition using YOLOv8 and deep learning models.

## Features
- Real-time license plate detection using YOLOv8 models
- License plate character recognition with trained neural networks
- Web-based interface for image processing and results visualization
- Multiple model versions for testing and comparison
- Clean, responsive design with FPT Education branding

## Project Structure
```
License-Plate-UI/
├── models/
│   ├── detection/            # License plate detection models (YOLOv8)
│   └── reader/               # Character recognition models
├── static/
│   ├── js/                   # Frontend JavaScript files
│   │   └── picture.js
│   ├── style.css             # Main stylesheet
│   ├── picture.css           # Additional styles for picture processing
│   └── uploads/              # User-uploaded images directory
├── templates/
│   ├── index.html            # Main application interface
│   └── picture.html          # Image processing results page
├── app.py                    # Main Flask application
├── detect_input_picture.py   # Input image processing script
└── read_LP.py                # License plate reading and recognition script
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/license-plate-recognition.git
   cd license-plate-recognition
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload an image containing a vehicle license plate through the interface

4. The system will:
   - Detect license plates in the image
   - Extract and recognize characters from detected plates
   - Display the results with bounding boxes and recognized text

## Dependencies
See `requirements.txt` for complete dependency list. Key packages include:
- Flask (web framework)
- OpenCV (computer vision)
- PyTorch (deep learning framework)
- Ultralytics YOLOv8 (object detection)
- Tesseract OCR (optical character recognition)

## Example Output
The system processes uploaded images and returns:
- Original image with detected license plates highlighted
- Recognized license plate text
- Confidence scores for detections
- Processing time information

## Model Performance

### License Plate Detection Models (YOLOv8)
The `Model_DetectorLP` directory contains 5 detection model versions with the following performance metrics:

| Version | mAP50 | mAP50-95 |
|---------|-------|----------|
| ver1    | 99.42% | 74.83%   |
| ver2    | 99.49% | 75.64%   |
| ver3    | 99.43% | 75.51%   |
| ver4    | 99.41% | 74.05%   |
| ver5    | 99.48% | 75.13%   |

**Key Findings:**
- All versions achieve excellent detection accuracy (>99.4% mAP50)
- ver2 performs best overall (mAP50-95: 75.64%)
- Models are trained on YOLOv8 architecture

### Character Recognition Models (YOLO11n)
The `Model_ReaderLP` directory contains character recognition models trained on 36 classes (digits 0-9, letters A-Z).

Training Configuration:
- **Architecture**: YOLO11n (nano variant)
- **Dataset**: 2,506 training images, 682 validation images
- **Classes**: 36 character classes
- **Image Size**: 640×640 pixels
- **Training Time**: ~55 minutes (45 epochs)
- **Hardware**: NVIDIA Tesla T4 GPU

Best Model Performance (45-epoch run):
- **mAP50**: 91.5%
- **mAP50-95**: 69.6%
- **Characters**: 2,589,172 parameters

Class-wise Performance Highlights:
- Perfect recognition (100%) for: A, F, G, H, L, M, P, S, T, V, X, Y, Z
- High accuracy (>95%): 0, 1, 2, 3, 4, 5, 6, 7, 9, B
- Lower accuracy: D, I, J, K, N, O, R

The model shows strong character recognition capabilities for most Vietnamese license plate characters.

## Model Files
Due to their large size, model files (.pt files) are not included in this repository by default (see `.gitignore`).
To use the system, you'll need to:
1. Place your trained YOLOv8 detection models in `models/detection/`
2. Place your trained character recognition models in `models/reader/`
3. Recommended: use the best-performing models based on the metrics above

## Testing Your Models
```python
# Verify model performance
from read_LP import load_and_test_model

# Test detection model
load_and_test_model('models/detection/LP_detect_ver5.pt')

# Test recognition model
load_and_test_model('models/reader/LP_reader_ver6.pt')
```

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments
- FPT Education for project support
- Ultralytics for YOLOv8 implementations
- OpenCV and PyTorch communities