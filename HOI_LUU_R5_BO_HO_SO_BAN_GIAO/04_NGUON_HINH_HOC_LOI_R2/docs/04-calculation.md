# 04 · Cơ sở tính và giới hạn công suất
ISO 8100-32 đề cập việc lập kế hoạch, chọn thang cho văn phòng/khách sạn/nhà ở [1]. CIBSE Guide D 2025 phân biệt tính toán và mô phỏng [2–3]. R2 thực hiện phép sàng lọc bằng hành trình ngẫu nhiên, chưa thực hiện mô phỏng hàng đợi hoặc điều phối.

Proxy net từng tầng văn phòng = **0,90 × (GFA sàn − quỹ lõi)**. Sau khi trừ lõi, 10% tiếp theo dự trữ cho tổn thất sử dụng còn lại. Đây là proxy để tính dân số, không phải NLA chứng nhận: các cột, phòng MEP ngoài lõi, sảnh ngoài lõi và tỷ lệ phân chia khách thuê chưa có mặt bằng hoàn chỉnh. Không áp hệ số 90% lên GFA rồi trừ lõi thêm lần nữa.

Dân số = proxy net /12 m²; nhu cầu =12% dân số/5 phút. Mục tiêu nghiên cứu R2 là interval văn phòng ≤35 s, shuttle ≤30 s, khách sạn ≤40 s. **Các số này là giả định mục tiêu của dự án, không phải trích dẫn yêu cầu ISO/QCVN.** Nếu muốn mức 30 s cho mọi nhóm văn phòng, nhiều nhóm hiện tại cần tăng xe hoặc đổi điều phối.

Tổng dân số proxy: A **13.060**, văn phòng D **2.908**. Các tầng hỗ trợ/MEP không bị gán dân số văn phòng; tải phụ trợ có thật vẫn phải bổ sung khi công năng được khóa.

Mỗi nhóm lấy 12.000 chuyến, seed cố định 20260929. Một chuyến có P hành khách chọn tầng theo tỷ lệ dân số, dừng theo thứ tự tăng cao độ, rồi trở về terminal. Thời gian flight dùng profile gia tốc 1 m/s²: với d nhỏ hơn v²/a là 2√(d/a), còn lại d/v+v/a. Cộng 7 s mỗi điểm dừng/terminal cho cửa và leveling, cộng 2×P×1 s cho boarding/alighting. Khách sạn dùng 8 s và 1,2 s. Profile chưa mô tả jerk; các thông số phải thay bằng đường cong hãng.

HC = 300×số xe×P / RTT. Interval = RTT/số xe. **Interval không phải thời gian chờ đo được**; cũng không được cộng HC local và HC shuttle để tuyên bố công suất đường đi. Một hành trình A trên cao bị giới hạn bởi mắt xích yếu nhất.

| Nhóm | Tầng phục vụ | Xe | P / chuyến | RTT s | Interval s | HC / nhu cầu, người/5 phút |
| --- | --- | --- | --- | --- | --- | --- |
| A-Z1-1 | 8–15 | 5 | 22 | 162.6 | 32.5 | 203 / 199 |
| A-Z1-2 | 16–23 | 5 | 22 | 174.4 | 34.9 | 189 / 187 |
| A-Z1-3 | 24–30 | 5 | 20 | 171.2 | 34.2 | 175 / 153 |
| A-Z2-1 | 33–40 | 5 | 22 | 149.3 | 29.9 | 221 / 167 |
| A-Z2-2 | 41–47 | 5 | 22 | 153.0 | 30.6 | 216 / 136 |
| A-Z2-3 | 48–54 | 5 | 22 | 163.2 | 32.6 | 202 / 124 |
| A-Z3-1 | 57–64 | 5 | 22 | 149.2 | 29.8 | 221 / 144 |
| A-Z3-2 | 65–71 | 5 | 22 | 152.9 | 30.6 | 216 / 117 |
| A-Z3-3 | 72–78 | 5 | 22 | 163.2 | 32.6 | 202 / 106 |
| A-Z4-1 | 81–89 | 5 | 22 | 158.7 | 31.7 | 208 / 131 |
| A-Z4-2 | 90–97 | 5 | 22 | 164.4 | 32.9 | 201 / 103 |
| D-LOW | 7–19 | 7 | 26 | 216.2 | 30.9 | 252 / 197 |
| D-HIGH | 21–33 | 7 | 26 | 235.7 | 33.7 | 232 / 152 |
| D-HOTEL | 37–61 | 7 | 16 | 267.0 | 38.1 | 126 / 84 |
| A-E2 | 01 → 32 | 6 | 33 | 129.4 | 21.6 | 459 / 427 |
| A-E3 | 01 → 56 | 6 | 33 | 151.2 | 25.2 | 393 / 367 |
| A-E4 | 01 → 80 | 6 | 33 | 173.0 | 28.8 | 343 / 234 |

![T02](../drawings/T02-traffic-screen.svg)

A-Z1-1 dự phòng khoảng 1.8%, A-Z1-2 khoảng 1.0%. Đây là mức rất mỏng, không nên khóa phương án như một hệ thống premium đã ổn định. Sai số lấy mẫu nhỏ không giải quyết được sai số giả định dân số, thời gian cửa hoặc lưu lượng người. Một ca thang ngừng hoạt động làm nhóm thấp A và một số tuyến shuttle thiếu công suất hoặc vượt interval.

Kịch bản 10 m² net/người làm ba nhóm local thấp A vượt HC; E2/E3 cũng thiếu công suất khi nâng dân số tương ứng. Mô hình cơ sở không được dùng cấp phép cho thuê mọi tầng ở mật độ 10 m²/người. Cần chạy cao điểm 15%, lunch/interfloor, mixed traffic, tải amenity và một xe ngừng hoạt động trong mô phỏng tiếp theo.
