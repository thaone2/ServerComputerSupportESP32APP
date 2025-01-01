import os
import sys
import time
import datetime
from firebase_admin import credentials, initialize_app, db

# Hàm lấy đường dẫn tuyệt đối khi chuyển sang .exe
def resource_path(relative_path):
    """Trả về đường dẫn tuyệt đối, tương thích với file .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Cấu hình Firebase
FIREBASE_HOST = "Link tới Realtime Database của bạn"
CRED_PATH = "Đường dẫn tới tệp Firebase của bạn .json"

# Khởi tạo Firebase
if not os.path.exists(CRED_PATH):
    raise FileNotFoundError("File credential Firebase không tồn tại!")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred, {"databaseURL": FIREBASE_HOST})

# Hàm chuyển đổi từ định dạng HH:MM:SS sang giây
def time_str_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(":"))
        return h * 3600 + m * 60 + s
    except ValueError:
        return 0  # Trả về 0 nếu định dạng không đúng

# Hàm định dạng thời gian (giây) thành HH:MM:SS
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Hàm lấy dữ liệu từ Firebase
def get_data_from_firebase(date, computer_id):
    ref = db.reference(f"/ComputerUsageTime/{date}/{computer_id}")
    data = ref.get()
    if data and "totalTime" in data:
        return time_str_to_seconds(data["totalTime"])  # Chuyển từ HH:MM:SS sang giây
    return 0

# Hàm gửi dữ liệu lên Firebase
def send_to_firebase(date, computer_id, total_time):
    ref = db.reference(f"/ComputerUsageTime/{date}/{computer_id}")
    formatted_time = format_time(total_time)  # Định dạng lại thành HH:MM:SS
    ref.set({"totalTime": formatted_time})
    print(f"Đã cập nhật dữ liệu lên Firebase cho {date}: {formatted_time}")

# Chương trình chính
if __name__ == "__main__":
    computer_id = "computer2"  # Đặt ID của máy tính
    today = str(datetime.date.today())

    # Lấy dữ liệu từ Firebase nếu có
    total_time = get_data_from_firebase(today, computer_id)

    print("Chương trình đang theo dõi thời gian sử dụng...")
    start_time = time.time()

    while True:
        # Chờ 20 giây trước lần cập nhật tiếp theo
        time.sleep(20)
        current_time = time.time()
        # Tính thời gian sử dụng trong chu kỳ 20 giây
        elapsed_time = current_time - start_time
        start_time = current_time  # Đặt lại thời điểm bắt đầu
        # Cộng dồn thời gian vào tổng
        total_time += elapsed_time
        # Gửi dữ liệu lên Firebase
        send_to_firebase(today, computer_id, int(total_time))
        # In thông báo
        total_time_formatted = format_time(int(total_time))
        print(f"Cập nhật: Tổng thời gian sử dụng hôm nay ({today}): {total_time_formatted}")