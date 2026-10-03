# HỘI LƯU R2

Mở HOI_LUU_R2.html để đọc hồ sơ và sáu bản vẽ vector.

R2 là nghiên cứu lõi/giao thông đứng sơ bộ. Vỏ, cao độ, ngân sách GFA giữ R1. Lõi/lỗ mở/B1 đã cập nhật trong data/geometry-r2.json. Các kiểm tra không phải chứng nhận thi công hoặc vận hành.

source-r1/ là nguồn tham chiếu, có OBJ chứa lõi/lỗ mở cũ. Không dùng OBJ đó như mô hình nội bộ R2. Chưa phát hành BIM/OBJ nội bộ R2.

Tái tạo: python scripts/build_r2.py rồi python scripts/build_drawings_report.py. Python + numpy, scipy, shapely, matplotlib, markdown. Seed và giả định được giữ trong r2-study.json.
