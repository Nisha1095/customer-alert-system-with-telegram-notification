# customer-alert-system-with-telegram-notification
This project implements a real-time human detection and alert system using OpenCV and the YOLOv3 object detection model, integrated with Telegram for instant notifications. The system processes video input (live camera or recorded footage) to detect the presence of humans and automatically sends alerts with timestamp details when a person is identified. It uses a confidence threshold to ensure accurate detection and includes a configurable alert interval to prevent repeated notifications within short durations.

The application is designed with a multi-threaded architecture, where one thread continuously performs object detection while another handles Telegram bot commands. Users can remotely control the system using /start and /stop commands via Telegram, enabling or disabling detection in real time. The system leverages asynchronous programming (asyncio) to send messages efficiently without interrupting the detection process.

This solution is particularly useful for security surveillance, smart shop monitoring, and unattended environments, providing immediate alerts when human activity is detected. The project is lightweight, customizable, and suitable for deployment on embedded platforms such as Raspberry Pi.

#<h2>Appreation Letter</h2>
<img src=""C:/Users/Nisha/Downloads/appreciation_letter.jpeg"" width="700">

<p>
This image shows the appreation letter received from the company for doing this project
</p>
<p>
This image shows the real-time human detection system identifying a customer entry through the CCTV video stream using the YOLOv3 model on Raspberry Pi 4.
</p>
