# 00 · HỘI LƯU R1 — Quyền ưu tiên dữ liệu và phạm vi

**Ngày phát hành: 30.09.2026 · Hệ mét · Thiết kế kiến trúc ở mức kiểm soát hình học.**

## Mục tiêu

Chuyển vision “A thuôn cao, D thấp hơn và thanh; đế mở về quảng trường chéo” thành một hệ hình học tái dựng được. A/D được thiết kế lại; vị trí tương đối, cấu hình duplex B/C và nguyên tắc mall B1 được kế thừa. Hồ sơ đủ để dựng mô hình khối, cao độ, biên sàn, lõi giữ chỗ, chân đế và crown theo cùng dữ liệu. Đây chưa phải mô hình BIM thi công, tính toán chịu lực hay hồ sơ cấp phép.

## Thứ tự ưu tiên khi có khác biệt

1. `data/geometry.json`: đường bao, cao độ, diện tích và vị trí công năng của lần phát hành R1.
2. `data/model-manifest.json`: quy tắc crown và chỗ lùi kính sky lobby dùng trong mô hình.
3. `data/floor-schedule.csv` và `data/outline-vertices.csv`: bảng kiểm tra và tọa độ xuất từ dữ liệu.
4. Bản vẽ SVG/PNG sinh bằng `scripts/build_views.py`.
5. Thuyết minh này; mọi kích thước làm tròn chỉ để đọc nhanh.
6. Phối cảnh GenAI trước đây: tham khảo cảm xúc và vật liệu, không được dùng đo tỷ lệ, số tầng, vị trí B/C hoặc diện tích.

Nếu phát hiện bất đồng giữa mục 1–4, dừng xuất bản bản dựng mới và sửa nguồn dữ liệu; không âm thầm nắn mô hình để giống ảnh.

## Trạng thái các quyết định

| Mức | Nội dung |
| --- | --- |
| Ràng buộc từ brief | Đất 295×155 m; FAR tối đa 14; mật độ tối đa 40%; B/C ≤40 tầng và 160 m; B2–B5 xe/kỹ thuật; mall B1 nối A/D, không vào đế B/C |
| Đường cơ sở R1 để dựng | A 98 tầng/480 m; D 62 tầng/285 m; tọa độ và profile trong JSON; 420.000 m² thân A/D; 50.000 m² đế A/D |
| Giữ chỗ kỹ thuật | Vùng lõi, tầng lánh nạn, MEP, liên kết cứng, ram và BOH; chưa xác nhận công suất hoặc kích thước thiết bị |
| Chưa xác lập | Hướng Bắc, mặt đường thật, chỉ giới thực tế, địa chất, mực nước, khảo sát gió, dân số tính toán, yêu cầu vận hành khách sạn |

## Các sửa đổi quan trọng so với lời mô tả trước

- A sử dụng hình chữ nhật bo góc có bốn rãnh lõm nông; diện tích chân tháp thực được tính từ đa giác, không lấy tròn 4.400 m².
- Tầng đế trên cùng A có đường bao 4.600 m², đủ bao chân thân tháp. 4.300 m² là sàn sau lỗ mở, không phải đường bao 3.000 m² như phương án phân bổ trước.
- Đế D trên cùng có đường bao 3.000 m²; sàn sau lỗ mở 2.850 m².
- A/D không xoay từng tầng. Mặt bằng co theo công thức; tâm tháp cố định.
- Crown là hệ gân/khung có cao độ rõ; không chứa thêm một số tầng vô hình ngoài bảng GFA.
- B/C trong OBJ chỉ là khối tham chiếu, không thay thế tài liệu duplex nguồn.

## Tham chiếu thiết kế

Đây là phương án tự phát triển từ các nguyên tắc tham khảo, không phải tài liệu của SOM. Nguồn chính đã nghiên cứu: [Tianjin CTF](https://www.som.com/projects/tianjin-ctf-finance-centre/), [One Century](https://www.som.com/projects/one-century/), [Manhattan West](https://www.som.com/projects/manhattan-west-development/), [Greenland Hangzhou Century Center](https://www.som.com/projects/greenland-hangzhou-century-center/). Tiếp thu quan hệ công năng–hình khối, biểu hiện kết cấu, sảnh mở và tính liên tục của mặt dựng; không sao chép tỷ lệ hay cấu kiện của một dự án cụ thể.
