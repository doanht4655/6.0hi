import os
import threading
import time
from flask import Flask
from javascript import require, On

# --- CẤU HÌNH ---
SERVER_IP = "bongx1.aternos.me"
SERVER_PORT = 48987
BOT_USERNAME = "Bot_Bedrock_Vip"

# --- WEB SERVER (Để Render không tắt) ---
app = Flask(__name__)

@app.route('/')
def index():
    return f"Bot {BOT_USERNAME} đang chạy!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BOT BEDROCK ---
bedrock = require('bedrock-protocol')

def run_bot():
    while True:
        try:
            print(f"[*] Dang ket noi toi {SERVER_IP}:{SERVER_PORT}...")
            
            # Cấu hình Client (Thụt đầu dòng chuẩn)
            client = bedrock.createClient({
                'host': SERVER_IP,
                'port': SERVER_PORT,
                'username': BOT_USERNAME,
                'offline': True,       # Bắt buộc cho Aternos Cracked
                'skipPing': True,      # Bỏ qua check ping để vào nhanh
                'version': 'latest'    # Thử dùng bản mới nhất
            })

            # Biến kiểm tra kết nối
            is_connected = False

            # Sự kiện khi vào Server thành công
            @On(client, 'spawn')
            def on_spawn(packet):
                nonlocal is_connected
                is_connected = True
                print(f"[+] {BOT_USERNAME} DA VAO SERVER!")
                
                # Hàm Anti-AFK: Chat mỗi 60 giây
                def chat_loop():
                    while is_connected:
                        try:
                            # Gửi tin nhắn chat để server biết bot còn sống
                            client.queue('text', {
                                'type': 'chat', 
                                'needs_translation': False, 
                                'source_name': client.username, 
                                'xuid': '', 
                                'platform_chat_id': '',
                                'message': "Bot treo may..."
                            })
                            print("[Action] Da gui chat chong AFK")
                            time.sleep(60)
                        except:
                            break
                
                # Chạy luồng chat riêng
                threading.Thread(target=chat_loop, daemon=True).start()

            # Sự kiện khi bị ngắt kết nối
            @On(client, 'close')
            def on_close(reason):
                nonlocal is_connected
                is_connected = False
                print(f"[-] Mat ket noi: {reason}")

            @On(client, 'error')
            def on_error(err):
                print(f"[!] Loi: {err}")

            # Vòng lặp giữ kết nối
            while True:
                time.sleep(1)
                # Nếu bot bị ngắt, thoát vòng lặp này để reconnect lại từ đầu
                if not is_connected:
                    break

        except Exception as e:
            print(f"[!] Loi khoi tao: {e}")
            time.sleep(10)

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    # Chạy Bot ở luồng phụ
    threading.Thread(target=run_bot, daemon=True).start()
    # Chạy Flask ở luồng chính
    run_flask()
                            
