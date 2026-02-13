const bedrock = require('bedrock-protocol')
const express = require('express')
const app = express()

// --- CẤU HÌNH SERVER ---
const options = {
  host: 'bongx1.aternos.me', // IP
  port: 48987,               // Port
  username: 'Bot_NodeJS_Vip', // Tên Bot
  offline: true,             // BẮT BUỘC: Server phải bật Cracked
  skipPing: true             // Bỏ qua ping để vào nhanh
}

// --- 1. WEB SERVER GIỮ RENDER SỐNG ---
app.get('/', (req, res) => {
  res.send('Bot Bedrock NodeJS đang chạy!')
})

const port = process.env.PORT || 3000
app.listen(port, () => {
  console.log(`Web server đang chạy ở port ${port}`)
})

// --- 2. BOT MINECRAFT ---
let client = null

function createBot() {
  console.log(`[*] Đang kết nối tới ${options.host}:${options.port}...`)

  client = bedrock.createClient(options)

  client.on('spawn', () => {
    console.log(`[+] ${options.username} ĐÃ VÀO SERVER!`)
    
    // Anti-AFK: Chat mỗi 60 giây
    setInterval(() => {
      if (client) {
        // Gửi gói tin text trực tiếp (nhẹ hơn hàm chat thường)
        try {
           client.queue('text', {
            type: 'chat', needs_translation: false, source_name: client.username, xuid: '', platform_chat_id: '',
            message: 'Bot NodeJS đang treo...'
          })
          console.log('[Info] Đã gửi chat chống AFK')
        } catch (e) {}
      }
    }, 60000)
  })

  client.on('disconnect', (packet) => {
    console.log('[-] Bị ngắt kết nối:', packet)
  })

  client.on('close', () => {
    console.log('[-] Kết nối bị đóng. Thử lại sau 20s...')
    setTimeout(createBot, 20000)
  })

  client.on('error', (err) => {
    console.log('[!] Lỗi:', err)
    // Lỗi thường gặp ở Bedrock, kệ nó, tự reconnect sau
  })
}

// Bắt đầu chạy bot
createBot()
        
