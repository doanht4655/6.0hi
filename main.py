import os
import threading
import time
import random
import math
from flask import Flask
from javascript import require, On, AsyncTask

# --- CẤU HÌNH SERVER ---
SERVER_IP = "bongx1.aternos.me"
SERVER_PORT = 48987
BOT_USERNAME = "BongX_SieuBot"

# --- PHẦN 1: FAKE WEB SERVER (Để Render không tắt) ---
app = Flask(__name__)

@app.route('/')
def index():
    return f"Bot {BOT_USERNAME} đang hoạt động với chế độ Anti-Detection v2.0"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- PHẦN 2: BOT THÔNG MINH ---
mineflayer = require('mineflayer')

# Danh sách các câu chat ngẫu nhiên (để giả người)
CHAT_MESSAGES = [
    "lag qua",
    "...",
    "server on roi",
    "treo ty nhe",
    "ai do cho xin it go",
    "ping cao the nhi"
]

def run_bot():
    while True:
        try:
            print(f"[*] Đang kết nối tới {SERVER_IP}:{SERVER_PORT}...")
            
            bot = mineflayer.createBot({
                'host': SERVER_IP,
                'port': SERVER_PORT,
                'username': BOT_USERNAME,
                'hideErrors': True,
                'version': False
            })

            # --- CÁC HÀM HÀNH VI CON NGƯỜI ---
            
            def look_around():
                # Quay đầu ngẫu nhiên (Yaw và Pitch)
                yaw = random.uniform(0, math.pi * 2)
                pitch = random.uniform(-math.pi/2, math.pi/2)
                bot.look(yaw, pitch)

            def walk_randomly():
                # Đi bộ ngẫu nhiên trong 1-2 giây rồi dừng
                direction = random.choice(['forward', 'back', 'left', 'right'])
                bot.setControlState(direction, True)
                time.sleep(random.uniform(0.5, 1.5)) 
                bot.setControlState(direction, False)

            def sneak_spam():
                # Ngồi xuống đứng lên (teabag)
                count = random.randint(2, 5)
                for _ in range(count):
                    bot.setControlState('sneak', True)
                    time.sleep(random.uniform(0.1, 0.3))
                    bot.setControlState('sneak', False)
                    time.sleep(random.uniform(0.1, 0.3))

            def swing_arm():
                # Đấm gió
                bot.swingArm()

            # --- LUỒNG CHÍNH CỦA BOT ---

            @On(bot, 'login')
            def login(this):
                print(f"[+] {BOT_USERNAME} ĐÃ VÀO SERVER (CHẾ ĐỘ ẨN DANH)")
                
                # Vòng lặp hành động ngẫu nhiên
                while True:
                    try:
                        # 1. Chọn hành động ngẫu nhiên
                        action = random.choice([
                            'look', 'look', 'look', # Tăng tỉ lệ nhìn quanh (an toàn nhất)
                            'walk', 
                            'jump', 
                            'sneak', 
                            'swing',
                            'chat'
                        ])

                        if action == 'look':
                            look_around()
                            print("[Action] Nhìn quanh")
                        elif action == 'walk':
                            walk_randomly()
                            print("[Action] Đi dạo")
                        elif action == 'jump':
                            bot.setControlState('jump', True)
                            time.sleep(0.5)
                            bot.setControlState('jump', False)
                            print("[Action] Nhảy")
                        elif action == 'sneak':
                            sneak_spam()
                            print("[Action] Ngồi lên ngồi xuống")
                        elif action == 'swing':
                            swing_arm()
                            print("[Action] Đấm gió")
                        elif action == 'chat':
                            # Chỉ chat 5% cơ hội để tránh spam
                            if random.random() < 0.05:
                                msg = random.choice(CHAT_MESSAGES)
                                bot.chat(msg)
                                print(f"[Action] Chat: {msg}")

                        # 2. Ngủ một khoảng thời gian NGẪU NHIÊN (Quan trọng nhất)
                        # Không bao giờ ngủ cố định 30s. Lúc 15s, lúc 60s, lúc 45s.
                        sleep_time = random.uniform(15, 90)
                        print(f"[*] Nghỉ {int(sleep_time)}s...")
                        time.sleep(sleep_time)

                    except Exception as e:
                        print(f"[!] Lỗi hành vi: {e}")
                        break

            @On(bot, 'end')
            def end(this, reason):
                print(f"[-] Kết nối bị ngắt: {reason}")

            @On(bot, 'error')
            def error(this, err):
                print(f"[!] Lỗi mạng: {err}")

            # Đợi trước khi reconnect (tránh bị ban IP do spam connect)
            time.sleep(random.uniform(10, 20))

        except Exception as e:
            print(f"[!] Crash tổng: {e}")
            time.sleep(30)

# --- CHẠY ---
if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    run_flask()
                          
