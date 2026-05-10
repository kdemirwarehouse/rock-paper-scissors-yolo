"""
Taş-Kağıt-Makas — YOLO ile Gerçek Zamanlı El Hareketi Tanıma
=============================================================
Webcam üzerinden el hareketlerini algılayıp bilgisayara karşı oynayan oyun.

Kontroller:
    Q : Çıkış
    R : Skoru sıfırla
"""

import cv2
import random
import time
from ultralytics import YOLO


# ---------- Ayarlar ----------
MODEL_YOLU = "best.pt"
KAMERA_INDEX = 0
GUVEN_ESIGI = 0.6
BEKLEME_SURESI = 2  # saniye

# ---------- Model ve kamera ----------
model = YOLO(MODEL_YOLU)
cap = cv2.VideoCapture(KAMERA_INDEX)

# ---------- Oyun durumu ----------
skor = {"Oyuncu": 0, "Bilgisayar": 0}
secenekler = ["tas", "kagit", "makas"]
son_oyun_zamani = 0
bilgisayar = None
sonuc = None


def kim_kazanir(oyuncu, bilgisayar):
    """Oyun sonucunu belirler ve skoru günceller."""
    if oyuncu == bilgisayar:
        return "Berabere"

    kazanan_durumlar = [("tas", "makas"), ("kagit", "tas"), ("makas", "kagit")]
    if (oyuncu, bilgisayar) in kazanan_durumlar:
        skor["Oyuncu"] += 1
        return "Kazandin"

    skor["Bilgisayar"] += 1
    return "Kaybettin"


# ---------- Ana döngü ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    results = model(frame, verbose=False)[0]

    oyuncu_secimi = None
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > GUVEN_ESIGI:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            class_name = results.names[int(class_id)].lower()

            if class_name in secenekler:
                oyuncu_secimi = class_name
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_name.upper(), (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                break

    suanki_zaman = time.time()
    if oyuncu_secimi and (suanki_zaman - son_oyun_zamani > BEKLEME_SURESI):
        bilgisayar = random.choice(secenekler)
        sonuc = kim_kazanir(oyuncu_secimi, bilgisayar)
        son_oyun_zamani = suanki_zaman

    if bilgisayar and (suanki_zaman - son_oyun_zamani < BEKLEME_SURESI):
        cv2.putText(frame, f"Bilgisayar: {bilgisayar}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"Sonuc: {sonuc}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        kalan = BEKLEME_SURESI - (suanki_zaman - son_oyun_zamani)
        cv2.putText(frame, f"Yeni oyun: {kalan:.1f} sn", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
    else:
        cv2.putText(frame, "Elinizi gosterin!", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.putText(frame,
                f"Skor - Sen: {skor['Oyuncu']}  PC: {skor['Bilgisayar']}",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Tas Kagit Makas", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):
        skor = {"Oyuncu": 0, "Bilgisayar": 0}

cap.release()
cv2.destroyAllWindows()
