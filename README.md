# customer-alert-system-with-telegram-notification
This project implements a real-time human detection and alert system using OpenCV and the YOLOv3 object detection model, integrated with Telegram for instant notifications. The system processes video input (live camera or recorded footage) to detect the presence of humans and automatically sends alerts with timestamp details when a person is identified. It uses a confidence threshold to ensure accurate detection and includes a configurable alert interval to prevent repeated notifications within short durations.

The application is designed with a multi-threaded architecture, where one thread continuously performs object detection while another handles Telegram bot commands. Users can remotely control the system using /start and /stop commands via Telegram, enabling or disabling detection in real time. The system leverages asynchronous programming (asyncio) to send messages efficiently without interrupting the detection process.

This solution is particularly useful for security surveillance, smart shop monitoring, and unattended environments, providing immediate alerts when human activity is detected. The project is lightweight, customizable, and suitable for deployment on embedded platforms such as Raspberry Pi.


The below video shows the working of the product during the customer entry or human detection.
https://github.com/user-attachments/assets/6822aae0-4eee-4c0b-a291-d47d6115f5cc

This video shows the working of the product under when no customer is detected.
https://github.com/user-attachments/assets/0e1d9483-dc54-47c2-a7a0-c8066dcdc255


