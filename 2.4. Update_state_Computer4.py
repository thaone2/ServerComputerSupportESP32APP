import sys
import os
import time
import socket
import firebase_admin
from firebase_admin import credentials, db

# Hàm để xử lý đường dẫn khi đóng gói thành file .exe
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Khi chạy từ file .exe
    except AttributeError:
        base_path = os.path.abspath(".")  # Khi chạy từ mã nguồn Python
    return os.path.join(base_path, relative_path)

# Cấu hình Firebase cấu hình firebase của bạn
FIREBASE_HOST = ""
cred_path = get_resource_path("")

try:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_HOST
    })
    print("Firebase initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Firebase: {e}")
    sys.exit(1)  # Thoát chương trình nếu không thể khởi tạo Firebase

# Hàm kiểm tra kết nối mạng
def is_connected(host="8.8.8.8", port=53, timeout=3):
    """Kiểm tra xem có kết nối mạng không bằng cách thử kết nối đến DNS Google."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Hàm kiểm tra trạng thái hiện tại trên Firebase
def get_current_status():
    try:
        device_id = "computer4"
        ref = db.reference(f'/Computer/{device_id}')
        data = ref.get()  # Lấy dữ liệu hiện tại
        if data and 'status' in data:
            return data['status']
        return 0  # Mặc định là 0 nếu không có dữ liệu
    except Exception as e:
        print(f"Failed to fetch current status: {e}")
        return None  # Trả về None nếu có lỗi

# Hàm cập nhật trạng thái bật máy lên Firebase
def update_online_status():
    try:
        current_status = get_current_status()
        if current_status is None:
            print("Unable to determine current status. Exiting...")
            return
        
        if current_status == 0:  # Chỉ cập nhật nếu trạng thái hiện tại là 0
            device_id = "computer4"
            ref = db.reference(f'/Computer/{device_id}')
            ref.set({'status': 1})  # Cập nhật trạng thái bật máy
            print(f"Updated {device_id} status to 1 (online) on Firebase.")
        else:
            print("Status is already 1 (online). No update needed.")
    except Exception as e:
        print(f"Failed to update status: {e}")

if __name__ == "__main__":
    print("Starting program...")
    while not is_connected():
        print("No network connection. Retrying in 5 seconds...")
        time.sleep(5)  # Đợi 5 giây trước khi thử lại

    print("Network connection established. Proceeding with Firebase update.")
    update_online_status()
