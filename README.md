# P2P
# FileSharing

Cách chạy chương trình:
Run: python3 Server.py
    - địa chỉ ip của máy trong mạng LAN được đặt cho server, ip sẽ được print tại terminal
     python3 Client.py <<ip-server>>

Người dùng có thể thao tác trên GUI hoặc CLI
CLI có các câu lệnh sau:
- Khi chưa đăng nhập
    - login <<username>> <<password>>
    - register <<username>> <<password>> <<repassword>>
- Khi đã đăng nhập với vai trò user
    - logout
    - publish <<lname>> <<fname>>
    - fetch <<fname>>
- Khi đã đăng nhập với vai trò user
    - ping <<username>>
    - discover <<username>>
    - logout