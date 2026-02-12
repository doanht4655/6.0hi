import os
import threading
import time
from flask import Flask
from javascript import require, On

# --- CẤU HÌNH SERVER BEDROCK ---
SERVER_IP = "bongx1.aternos.me"
SERVER_PORT = 48987 # Port Bedrock thường là số 5 chữ số
BOT_USERNAME = "Bot_Bedrock_Vip"

# --- WEB SERVER GIẢ (GIỮ RENDER SỐNG) ---
app = Flask(__name__)

@app.route('/')
def index():
    return f"Bot Bedrock {BOT_USERNAME} đang hoạt động!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- PHẦN CODE BOT BEDROCK ---
bedrock = require('bedrock-protocol')

def run_bot():
    while True:
        try:
            print(f"[*] Đang kết nối tới Server Bedrock: {SERVER_IP}:{SERVER_PORT}...")
            
            # Tạo client kết nối
            client = bedrock.createClient({
                'host': SERVER_IP,
                'port': SERVER_PORT,
                'username': BOT_USERNAME,
                'offline': True, # BẮT BUỘC: Server phải bật Cracked
                'skipPing': True # Bỏ qua check ping để vào nhanh hơn
            })

            # Biến kiểm tra trạng thái
            is_connected = False

            # Sự kiện khi kết nối thành công (spawn)
            @On(client, 'spawn')
            def on_spawn(packet):
                nonlocal is_connected
                if not is_connected:
                    print(f"[+] {BOT_USERNAME} ĐÃ VÀO SERVER THÀNH CÔNG!")
                    is_connected = True
                    
                    # Vòng lặp Anti-AFK (Chat mỗi 60s)
                    def anti_afk_loop():
                        while is_connected:
                            try:
                                # Gửi packet chat để server biết mình còn sống
                                # (Bot Bedrock không nhảy được, nên phải dùng chat)
                                msg = "Bot đang treo máy..."
                                client.queue('text', {
                                    'type': 'chat', 
                                    'needs_translation': False, 
                                    'source_name': client.username, 
                                    'xuid': '', 
                                    'platform_chat_id': '',
                                    'message': msg
                                })
                                print("[Action] Bot vừa chat chống AFK")
                                time.sleep(60)
                            except:
                                break
                    
                    # Chạy luồng Anti-AFK riêng
                    threading.Thread(target=anti_afk_loop, daemon=True).start()

            # Sự kiện khi bị ngắt kết nối
            @On(client, 'close')
            def on_close(reason):
                nonlocal is_connected
                is_connected = False
                print(f"[-] Bot bị ngắt kết nối. Lý do: {reason}")

            @On(client, 'error')
            def on_error(err):
                print(f"[!] Lỗi: {err}")

            # Giữ kết nối trong vòng lặp này
            while True:
                time.sleep(1)
                # Nếu bot bị disconnect thì thoát vòng lặp để reconnect
                if not is_connected and "client" in locals() and hasattr(client, 'status') and client.status == 1: 
                     # status 1 là disconnected trong một số phiên bản, nhưng an toàn nhất là dựa vào event close
                     pass

        except Exception as e:
            print(f"[!] Lỗi khởi tạo: {e}")
            time.sleep(20)

# --- CHẠY ---
if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    run_flask()
            
