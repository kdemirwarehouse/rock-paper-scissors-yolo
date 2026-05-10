# 🪨📄✂️ Rock-Paper-Scissors — Real-Time Hand Gesture Recognition with YOLO

A computer vision project that lets you play **Rock-Paper-Scissors** against the computer using real-time hand gesture detection via your webcam.  
Hand signs (rock, paper, scissors) are detected using a custom-trained **YOLO model** (`best.pt`), the opponent's move is chosen randomly, and the score is tracked live on screen.

---

## ✨ Features

- 🎥 **Real-time hand gesture recognition** via webcam
- 🤖 **Custom-trained YOLO model** for high-accuracy classification
- 🧠 Automatic opponent (computer) move selection
- 🏆 Live **score tracking** (Player / Computer)
- ⏱️ Cooldown between rounds for a smooth gameplay experience
- 🔄 Reset score with a single key

---

## 📸 Screenshot

> You can add a screenshot from the game here:  
> `![Gameplay](docs/screenshot.png)`

---

## 🛠️ Tech Stack

| Technology | Description |
|------------|-------------|
| **Python 3.8+** | Main programming language |
| **Ultralytics YOLO** | Object detection framework |
| **OpenCV** | Image processing and webcam capture |
| **PyTorch** | Backend for the YOLO model |

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/kdemirwarehouse/tas-kagit-makas-yolo.git
cd tas-kagit-makas-yolo
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add the model file
Place your trained `best.pt` file in the project's root directory.

---

## ▶️ Usage

```bash
python main.py
```

Once the webcam opens, show your hand to the camera — the system will detect your gesture and play against the computer.

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the game |
| `R` | Reset the score |

---

## 🧠 About the Model

The model is trained on three classes:
- `tas` 🪨 (rock)
- `kagit` 📄 (paper)
- `makas` ✂️ (scissors)

The confidence threshold is set to `0.6` by default. You can change this value inside `main.py`.

> Want to train your own model? Check out the [Ultralytics YOLO Training Guide](https://docs.ultralytics.com/modes/train/).

---

## 📁 Project Structure

```
tas-kagit-makas-yolo/
│
├── main.py              # Main game file
├── best.pt              # Trained YOLO model
├── requirements.txt     # Dependencies
├── README.md            # This file
├── .gitignore
└── LICENSE
```

---

## 🔧 Possible Improvements

- [ ] Add a round limit (e.g. best of 5)
- [ ] Add sound effects
- [ ] More gestures (e.g. Spock, lizard — Rock-Paper-Scissors-Lizard-Spock)
- [ ] Multiplayer mode
- [ ] Save scores to a file
- [ ] GUI with PyQt or Tkinter

---

## 🤝 Contributing

Contributions are always welcome!
1. Fork the project
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push your branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Kadir Demir**  
- GitHub: [@kdemirwarehouse](https://github.com/kdemirwarehouse)
- LinkedIn: [Kadir Demir](https://www.linkedin.com/in/kadir-demir-0a236a31b)

---

⭐ If you liked this project, don't forget to give it a star!
