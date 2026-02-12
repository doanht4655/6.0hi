import os
import threading
import time
from flask import Flask
from javascript import require, On

# --- CẤU HÌNH ---
SERVER_IP = "bongx1.aternos.me"
SERVER_PORT = 48987 # Check lại port trên Aternos xem có đổi ko
BOT_USERNAME = "Bot_BongX_Vip"

app = Flask(__name__)
@app.route('/')
def index(): return "Bot Bedrock Online!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# --- CODE BOT BEDROCK ---
bedrock = require('bedrock-protocol')

def run_bot():
    while True:
        try:
            print(f"[*] Đang kết nối tới {SERVER_IP}:{SERVER_PORT}...")
            
            client = bedrock.createClient({
                'host': SERVER_IP,
                'port': SERVER_PORT,
                'username': BOT_USERNAME,
                'offline': True,       # Bắt buộc cho server Cracked
                'skipPing': True,      # Bỏ qua check ping để vào nhanh
                'version': 'latest'    # Cố gắng dùng bản mới nhất
            })

            is_connected = False

            @On(client, 'spawn')
            def on_spawn(packet):
                nonlocal is_connected
                is_connected = True
                print(f"[+] {BOT_USERNAME} ĐÃ VÀO SERVER!")
                
                # Chat mỗi 30s để server biết bot còn sống
                def chat_loop():
                    while is_connected:
                        try:
                            # Gửi packet text thay vì client.queue('text') hay lỗi
                            client.queue('text', {
                                'type': 'chat', 'needs_translation': False, 
                                'source_name': client.username, 'xuid': '', 
                                'platform_chat_id': '', 'message': "Bot treo..."
                            })
                            time.sleep(30)
                        except: break
                threading.Thread(target=chat_loop, daemon=True).start()

            @On(client, 'disconnect') # Bắt lỗi disconnect cụ thể
            def on_disconnect(packet):
                print(f"[-] Bị kick: {packet}")
                nonlocal is_connected
                is_connected = False

            @On(client, 'close')
            def on_close(reason):
                print(f"[-] Đóng kết nối: {reason}")
                nonlocal is_connected
                is_connected = False

            @On(client, 'error')
            def on_error(err):
                print(f"[!] Lỗi: {err}")

            # Giữ connection
            while True:
                time.sleep(1)
                if not is_connected and getattr(client, 'status', 0) == 1: # Check trạng thái đóng
                    break

        except Exception as e:
            print(f"[!] Crash: {e}")
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    run_flask()
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
            
