# 02 · Hệ tọa độ, tổng mặt bằng và giao tiếp

Gốc tại góc khu đất (0;0). X dọc cạnh 295 m; Y dọc cạnh 155 m; Z hướng lên, ±0,00 tại nền tiếp cận giả định. **Không gắn X/Y với Đông/Tây/Bắc/Nam.** Đơn vị tất cả tọa độ là mét. Không tự thêm cốt nền +1,10 m từ một dự án khác.

| Tháp | Tâm X | Tâm Y | Góc xoay |
| --- | --- | --- | --- |
| A | 53 | 49 | 0° (B/C theo phép biến đổi nguồn) |
| B | 124 | 120 | 0° (B/C theo phép biến đổi nguồn) |
| C | 164 | 35 | 0° (B/C theo phép biến đổi nguồn) |
| D | 238 | 104 | 0° (B/C theo phép biến đổi nguồn) |

![S01 — Biên đế, chân tháp, tuyến quảng trường và vùng riêng tư.](../drawings/S01-site.svg)

*S01 — Biên đế, chân tháp, tuyến quảng trường và vùng riêng tư.*

## B/C giữ nguyên

B: X=94+u, Y=102+v. C: X=194−u, Y=53−v. Polygon local gồm (0,0),(32,0),(32,6),(60,6),(60,36),(28,36),(28,30),(0,30). Footprint 1.824 m²/tháp. Mỗi tháp 92 căn duplex, 40 tầng vật lý, mái +154,20 m, crown +158,70 m.

Các lõi và phần chia căn của B/C lấy từ `bc-source-r1.json`; mô hình tổng thể chỉ dựng đường bao để kiểm tra tương quan. Ngân sách đế B/C 14.000 m²/tháp chưa được chia thành mặt bằng mới trong gói này.

## A/D và quảng trường

Tâm A=(53;49), tâm D=(238;104). Hai trục tháp không nghiêng và không xoay theo tầng. Các đế có tâm dịch dần về tâm tháp khi lên cao, tạo khoảng lùi về phía quảng trường.

Tim tuyến đi bộ kiểm soát: (80;70) → (112;79) → (167;78) → (208;82) → (229;93). Vùng tuyến rộng cơ sở 24 m, cắt khỏi các đế và vùng đệm B/C. Phần tim đi vào đế A/D chỉ định hướng sảnh mall; phần quảng trường ngoài trời là polygon còn lại trong JSON.

Vùng đệm 6 m quanh đế B/C là lựa chọn bố trí riêng tư, không phải khoảng cách pháp quy đã xác nhận. Khi triển khai đường xe chữa cháy, đường dạo và cây xanh, cần phân định lại từng dải.

## Khoảng cách hình học ngắn nhất giữa chân các thân tháp

| Cặp tháp | Khoảng cách m |
| --- | --- |
| A–D | 122,27 |
| A–B | 26,19 |
| A–C | 46,00 |
| D–B | 54,00 |
| D–C | 34,87 |
| B–C | 55,58 |

Đây là khoảng cách giữa polygon mặt đứng ngoài chân tháp, không phải kết luận đạt yêu cầu chiếu sáng, riêng tư, thoát nạn hoặc cứu hỏa. A–B là cặp cần khảo sát kỹ nhất khi triển khai mặt dựng và loggia B. Chưa có hướng địa lý nên chưa xác lập hướng che nắng hay cửa nhìn.

## Tiếp cận vận hành

- A: sảnh văn phòng tiếp cận từ mép ngoài khu đất; cửa mall hướng vào quảng trường. Hai tuyến chỉ giao tiếp qua ranh kiểm soát rõ.
- D: tách cửa văn phòng, cửa khách sạn và đường phục vụ; sảnh khách sạn không sử dụng hành lang mall làm tuyến đến bắt buộc.
- B/C: tiếp cận cư dân từ phía ngoài cụm; không mở sảnh mall, thang cuốn hoặc cửa thoát dòng thương mại qua đế căn hộ.
- Hai vùng ram là giữ chỗ mặt bằng. Đấu nối với đường công cộng chỉ được chốt sau khi có hồ sơ mặt đường thật.
