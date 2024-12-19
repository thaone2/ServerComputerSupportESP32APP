import os
import json
import time
import datetime
from firebase_admin import credentials, initialize_app, db

# Cấu hình Firebase
FIREBASE_HOST = "Link tới Realtime Database của bạn"
CRED_PATH = "Đường dẫn tới tệp Firebase .json"

# File lưu trữ thời gian local
LOCAL_STORAGE = "usage_time.json"

# Khởi tạo Firebase
if not os.path.exists(CRED_PATH):
    raise FileNotFoundError("File credential Firebase không tồn tại!")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred, {"databaseURL": FIREBASE_HOST})

# Hàm đọc dữ liệu từ file JSON
def load_local_data():
    if not os.path.exists(LOCAL_STORAGE):
        return {}
    with open(LOCAL_STORAGE, "r") as file:
        return json.load(file)

# Hàm lưu dữ liệu vào file JSON
def save_local_data(data):
    with open(LOCAL_STORAGE, "w") as file:
        json.dump(data, file, indent=4)

# Hàm gửi dữ liệu lên Firebase
def send_to_firebase(date, computer_id, total_time):
    ref = db.reference(f"/ComputerUsageTime/{date}/{computer_id}")
    ref.set({"totalTime": total_time})
    print(f"Đã cập nhật dữ liệu lên Firebase cho {date}: {total_time}")

# Hàm định dạng thời gian (giây) thành HH:MM:SS
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Chương trình chính
if __name__ == "__main__":
    computer_id = "computer2"  # Đặt ID của máy tính
    today = str(datetime.date.today())

    # Tải dữ liệu local
    data = load_local_data()

    # Kiểm tra ngày hôm nay trong dữ liệu
    if today not in data:
        data[today] = {}

    if computer_id not in data[today]:
        data[today][computer_id] = 0

    try:
        print("Chương trình đang theo dõi thời gian sử dụng...")
        start_time = time.time()

        while True:
            # Chờ 60 giây trước lần cập nhật tiếp theo
            time.sleep(20)
            current_time = time.time()

            # Tính thời gian sử dụng trong chu kỳ 60 giây
            elapsed_time = current_time - start_time
            start_time = current_time  # Đặt lại thời điểm bắt đầu

            # Cộng dồn thời gian vào tổng
            data[today][computer_id] += elapsed_time
            save_local_data(data)

            # Gửi dữ liệu lên Firebase
            total_time_formatted = format_time(int(data[today][computer_id]))
            send_to_firebase(today, computer_id, total_time_formatted)

            print(f"Cập nhật: Tổng thời gian sử dụng hôm nay ({today}): {total_time_formatted}")

    except KeyboardInterrupt:
        print("\nKết thúc theo dõi.")
