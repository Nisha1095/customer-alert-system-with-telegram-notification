import cv2
import time
import threading
import numpy as np
import asyncio

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =======================
# TELEGRAM CONFIG
# =======================
BOT_TOKEN = "7809821610:AAG4ZIjk2oNFLVKZ0nOZegzBz-tdkLkaiwg"
CHAT_ID = 6442054015

# =======================
# GLOBAL FLAGS
# =======================
DETECTION_ENABLED = False
LAST_ALERT_TIME = 0

# =======================
# VIDEO CONFIG
# =======================
VIDEO_PATH = "/home/pi/person_detection/human_video2.mp4"
FRAME_SKIP = 30
CONFIDENCE = 0.5
ALERT_INTERVAL = 30

# =======================
# LOAD YOLOv3
# =======================
print("📦 Loading YOLOv3 (OpenCV DNN)...")
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# =======================
# CREATE GLOBAL BOT INSTANCE
# =======================
bot = Bot(token=BOT_TOKEN)

# =======================
# ASYNC MESSAGE SENDER
# =======================
async def send_async_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print("⚠ Telegram send failed:", e)

# =======================
# TELEGRAM COMMANDS
# =======================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global DETECTION_ENABLED
    DETECTION_ENABLED = True
    await update.message.reply_text("▶️ Detection STARTED.")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global DETECTION_ENABLED
    DETECTION_ENABLED = False
    await update.message.reply_text("⏹ Detection STOPPED.")

# =======================
# TELEGRAM THREAD
# =======================
def run_telegram_bot():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stop", stop_command))

    print("🤖 Telegram bot running...")
    app.run_polling()

# =======================
# DETECTION THREAD
# =======================
def run_detection():
    global LAST_ALERT_TIME

    cap = cv2.VideoCapture(VIDEO_PATH)
    frame_id = 0

    print("🎥 Detection thread started...")

    while True:

        if not DETECTION_ENABLED:
            time.sleep(1)
            continue

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame_id += 1
        if frame_id % FRAME_SKIP != 0:
            continue

        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (416, 416), swapRB=True, crop=False
        )
        net.setInput(blob)
        outputs = net.forward(output_layers)

        person_count = 0

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if classes[class_id] == "person" and confidence > CONFIDENCE:
                    person_count += 1

        current_time = time.time()

        if person_count > 0 and (current_time - LAST_ALERT_TIME) >= ALERT_INTERVAL:

            message = (
                f"🚨 HUMAN DETECTED!\n"
                f"👤 Persons: {person_count}\n"
                f"⏱ {time.strftime('%H:%M:%S')}"
            )

            print("📩 Sending alert...")

            # Run async safely inside thread
            try:
                asyncio.run(send_async_message(message))
            except Exception as e:
                print("⚠ Async error:", e)

            LAST_ALERT_TIME = current_time


# =======================
# MAIN START
# =======================
if __name__ == "__main__":

    # Start detection thread
    detection_thread = threading.Thread(
        target=run_detection,
        daemon=True
    )
    detection_thread.start()

    # Run telegram in main thread
    run_telegram_bot()
