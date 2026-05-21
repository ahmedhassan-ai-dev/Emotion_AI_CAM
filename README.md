# 🎭 Real-Time Emotion Detection System
### ESP32-CAM · Flask · Vision Transformer · Live Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32--CAM-Embedded-E7352C?style=for-the-badge&logo=espressif&logoColor=white)

---

## 📌 Overview

An **end-to-end, low-cost, real-time** facial emotion recognition pipeline built on an ESP32-CAM and a Flask inference server. Frames are captured at the edge, transmitted over Wi-Fi, classified by a fine-tuned **Vision Transformer (ViT)**, and visualised on an interactive live dashboard — all with **sub-second round-trip latency** on a local network.

> ✅ Multi-face support &nbsp;|&nbsp; ✅ Sub-second latency &nbsp;|&nbsp; ✅ Live dashboard &nbsp;|&nbsp; ✅ CSV export

---

## 🏗️ System Architecture

```
ESP32-CAM                Flask Server               Dashboard
──────────               ────────────               ─────────
 Capture frame  ──────►  Receive image   ──────►   Chart.js
 Preprocess     HTTP POST  OpenCV detect           Pie chart
 Send image      JSON     ViT inference            Timeline
                          Softmax + label  ◄──────  CSV export
                          Return result
```

**Pipeline:**
`Capture → Transmit → Face Detection → ViT Inference → Softmax & Threshold → Store & Visualise`

- **Ngrok** used for secure tunnelling during development / remote device testing
- **CSV / SQLite** for lightweight persistence and experiment logs

---

## 🎯 Features

| Feature | Details |
|---|---|
| 🤖 **AI Model** | Pretrained ViT fine-tuned for facial emotion recognition |
| 😀 **Emotion Classes** | Happy, Sad, Angry, Neutral, Fear, Disgust, Surprise (7 classes) |
| 📸 **Edge Capture** | ESP32-CAM with optional on-device preprocessing |
| 🖥️ **Dashboard** | Live pie chart + emotion timeline (Chart.js) |
| ⚡ **Optimisations** | Batching, half-precision (FP16) inference, input resizing |
| 💾 **Storage** | CSV & SQLite for session logging and export |
| 🔒 **Tunnelling** | Ngrok for remote development and testing |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Embedded** | ESP32-CAM (Arduino / ESP-IDF) |
| **Backend** | Python 3.9+, Flask |
| **AI / ML** | HuggingFace Transformers, Vision Transformer (ViT) |
| **Computer Vision** | OpenCV (face detection, ROI extraction) |
| **Frontend** | Chart.js (pie chart, timeline) |
| **Storage** | CSV, SQLite |
| **Networking** | Ngrok (dev tunnelling) |

---

## 📁 Project Structure

```
emotion-detection/
├── esp32/
│   └── esp32_cam_client.ino      # ESP32-CAM firmware (capture + HTTP POST)
├── server/
│   ├── app.py                    # Flask API — main inference endpoint
│   ├── model.py                  # ViT model loading & inference
│   ├── detector.py               # OpenCV face detection & ROI extraction
│   └── storage.py                # CSV / SQLite logging
├── dashboard/
│   ├── templates/
│   │   └── index.html            # Live dashboard UI
│   └── static/
│       └── charts.js             # Chart.js visualisations
├── data/
│   └── sessions/                 # Saved CSV session logs
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/emotion-detection-esp32.git
cd emotion-detection-esp32
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Flash ESP32-CAM firmware
- Open `esp32/esp32_cam_client.ino` in Arduino IDE
- Set your Wi-Fi credentials and Flask server URL:
```cpp
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_SERVER_IP:5000/predict";
```
- Select board: `AI Thinker ESP32-CAM` → Upload

### 4. Run the Flask server
```bash
python server/app.py
```

### 5. (Optional) Enable remote access with Ngrok
```bash
ngrok http 5000
```
Update the `serverUrl` in the ESP32 firmware with the Ngrok URL.

### 6. Open the dashboard
Navigate to `http://localhost:5000` in your browser.

---

## 🔌 API Reference

### `POST /predict`
Accepts a JPEG image and returns an emotion classification.

**Request:**
```
Content-Type: image/jpeg
Body: raw JPEG bytes
```

**Response:**
```json
{
  "timestamp": "2025-05-22T14:30:00Z",
  "faces": [
    {
      "bbox": [x, y, w, h],
      "emotion": "happy",
      "confidence": 0.92,
      "probabilities": {
        "happy": 0.92,
        "neutral": 0.05,
        "sad": 0.02,
        "angry": 0.005,
        "surprise": 0.003,
        "fear": 0.001,
        "disgust": 0.001
      }
    }
  ]
}
```

### `GET /history`
Returns stored emotion events for dashboard rendering.

### `GET /export`
Downloads session data as CSV.

---

## 📊 Results

From a demo session (local network):

| Emotion | Distribution |
|---|---|
| 😊 Happy | 40% |
| 😐 Neutral | 30% |
| 😲 Surprise | 10% |
| 😢 Sad | 8% |
| 😠 Angry | 7% |
| 😨 Fear | 3% |
| 🤢 Disgust | 2% |

- **Latency:** Sub-second round-trip on local network
- **Multi-face:** Supported
- **Dashboard:** Live updates via polling (WebSocket planned)

---

## 🚧 Known Limitations

- Edge compute constraints on ESP32-CAM limit on-device processing
- Accuracy affected by varying lighting conditions and face occlusions
- Class imbalance may reduce performance on less-common emotions (Fear, Disgust)
- Current polling-based refresh adds minor latency to dashboard updates

---

## 🔮 Future Improvements

- [ ] Replace polling with **WebSocket / RTSP** for lower-latency streaming
- [ ] Implement **face tracking** to maintain identity across frames
- [ ] **Quantise model** or export to **ONNX / TFLite** for on-device inference
- [ ] Build a **mobile app** for remote monitoring and alerts
- [ ] Add **data augmentation** pipeline to address class imbalance
- [ ] Support **multiple ESP32-CAM** nodes simultaneously

---

## 📋 Requirements

```
flask>=2.0
opencv-python>=4.5
transformers>=4.30
torch>=2.0
Pillow>=9.0
numpy>=1.23
pyngrok>=5.0
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙋 Contact

Questions or collaborations? Reach out via:
- 📧 Email:v ahmedhassan2062005@gmail.com
- 💼 LinkedIn: www.linkedin.com/in/ahmed-hassan-mohamed01
- 🐙 GitHub: https://github.com/ahmedhassan-ai-dev

---

<p align="center">
  Built with ❤️ at the intersection of <strong>IoT</strong> and <strong>AI</strong>
</p>
