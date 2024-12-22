# GihanIT Advanced Background Remover

A professional desktop application that automatically removes backgrounds from images using advanced computer vision techniques. The application provides an intuitive graphical user interface with real-time preview and adjustable controls for fine-tuning the results.

## Features

- User-friendly graphical interface
- Real-time image preview
- Adjustable processing controls
- Support for multiple image formats
- Progress tracking during processing
- One-click background removal
- High-quality output with transparency
- Save results in PNG format with transparency

## Download and Installation

### For End Users (Windows)

1. Go to the [Releases](link-to-your-releases) section
2. Download the latest `GihanIT Background Remover.exe`
3. Double-click the downloaded file to run the application
   - No installation or setup required
   - No need to install Python or any dependencies

### For Developers

If you want to run from source code or contribute to development, you'll need:

- Python 3.x (3.7 or later recommended)
- Required packages: opencv-python, Pillow, numpy

Install dependencies:
```bash
pip install -r requirements.txt
```

Run from source:
```bash
python background_remover.py
```

## Usage

1. Start the application:
   - Double-click the .exe file (for end users)
   - OR run the Python script (for developers)

2. Using the application:
   - Click "Choose Image" to select an image file
   - Adjust the processing controls as needed:
     - Threshold: Controls background detection sensitivity
     - Edge Sensitivity: Adjusts edge detection precision
     - Detail Level: Fine-tunes detail preservation
   - Click "Remove Background" to process the image
   - Once processing is complete, click "Save Image" to save the result

## Processing Controls

- **Threshold (0.0 - 1.0)**: Adjusts how aggressive the background removal is. Higher values remove more of the background but might affect the subject.
- **Edge Sensitivity (0.0 - 1.0)**: Controls how the algorithm detects edges between the subject and background. Higher values detect more subtle edges.
- **Detail Level (0.0 - 1.0)**: Determines how much fine detail is preserved in the final image. Higher values retain more details but might keep some background elements.

## Output

The processed images are saved in PNG format with transparency. The default filename adds "_no_bg" to the original filename.

## Troubleshooting

Common issues and solutions:

1. **Antivirus Warning**: Some antivirus software might flag the .exe file. This is a false positive due to the packaging method. The application is safe to use.

2. **Windows SmartScreen**: If you see a Windows SmartScreen warning, you can click "More info" and then "Run anyway" to start the application.

3. **Image Loading Error**: Ensure the image format is supported (PNG, JPG, JPEG)

4. **Memory Error**: Try processing a smaller image or resize the image before processing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for computer vision capabilities
- Python tkinter for GUI framework
- PIL (Python Imaging Library) for image processing