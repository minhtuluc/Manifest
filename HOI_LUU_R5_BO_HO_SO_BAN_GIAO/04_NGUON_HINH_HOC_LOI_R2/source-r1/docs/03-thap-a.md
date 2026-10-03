# 03 · Tháp A — hình học, cao độ và tổ chức công năng

**98 tầng vật lý = 6 tầng đế + 92 tầng thân. Thân 300.000 m²; đế 28.000 m².** Mái kết cấu kiểm soát +452,40 m; đỉnh kiến trúc +480,00 m. Không tính crown thành tầng khai thác bổ sung.

## Luật tạo hình tái dựng được

Tại cao độ z trong đoạn 34,00–452,40 m:

```text
t = clamp((z−34,00)/418,40, 0, 1)
q = t ^ 1.205238426409
W = 70 × (1−0,28q)
H = 66 × (1−0,34q)
R = 16 × (1−0,30q)
d = (1,2+0,4 sin(πt)) × (1−0,30q)
```

Tạo hình chữ nhật bo góc W×H, bán kính R. Lấy 256 điểm theo chiều dài chu vi, bắt đầu tại trung điểm mặt +X, chạy ngược chiều kim đồng hồ. Với mỗi điểm local (u,v), đặt θ=atan2(v,u); Δ là khoảng góc nhỏ nhất tới một trong bốn trục 0°,90°,180°,270°. Co bán kính của điểm một lượng `d × exp[−(Δ/0,14)²]`. Quy tắc này tạo bốn rãnh lõm nông giữa bốn mặt. Sau đó cộng tâm (53;49).

Số mũ được giải bằng tổng diện tích của các tầng thật, có trừ ba lỗ mở 96 m²; không nội suy từ một diện tích sàn trung bình. Đường bao chân thân A tại A07 có diện tích 4.359,57 m². Kích thước W/H là kích thước hạt giống bo góc, không đồng nhất tuyệt đối với bounding box sau biến dạng.

## Các mốc kiểm tra

| Tầng | Z m | Cao tầng m | W m | H m | Sàn m² | Công năng |
| --- | --- | --- | --- | --- | --- | --- |
| A07 | 34,00 | 6,00 | 70,00 | 66,00 | 4.359,57 | Sky lobby/support |
| A30 | 136,80 | 4,40 | 66,39 | 61,87 | 3.866,72 | Office |
| A31 | 141,20 | 6,00 | 66,20 | 61,65 | 3.842,16 | MEP/refuge/outrigger reservation |
| A32 | 147,20 | 6,00 | 65,95 | 61,36 | 3.712,48 | Sky lobby/support |
| A54 | 245,60 | 4,40 | 61,38 | 56,13 | 3.239,56 | Office |
| A55 | 250,00 | 6,00 | 61,17 | 55,89 | 3.213,84 | MEP/refuge/outrigger reservation |
| A56 | 256,00 | 6,00 | 60,87 | 55,55 | 3.082,77 | Sky lobby/support |
| A78 | 354,40 | 4,40 | 55,79 | 49,73 | 2.609,95 | Office |
| A79 | 358,80 | 6,00 | 55,56 | 49,46 | 2.584,98 | MEP/refuge/outrigger reservation |
| A80 | 364,80 | 6,00 | 55,23 | 49,09 | 2.455,00 | Sky lobby/support |
| A97 | 441,20 | 4,40 | 51,03 | 44,28 | 2.128,29 | Office |
| A98 | 445,60 | 6,80 | 50,78 | 44,00 | 2.104,57 | MEP/refuge/outrigger reservation |

![A01 — Bốn mặt bằng A cùng tỷ lệ; lõi là vùng giữ chỗ.](../drawings/A01-plans.svg)

*A01 — Bốn mặt bằng A cùng tỷ lệ; lõi là vùng giữ chỗ.*

## Tầng và chiều cao

A01–A06 là đế, tổng cao 34 m. Tầng thân điển hình cao 4,40 m. A07, A31, A32, A55, A56, A79, A80 cao 6,00 m; A98 cao 6,80 m. Các tầng còn lại giữ 4,40 m. CSV cung cấp đủ 98 dòng, không bỏ số tầng vì lý do thương mại.

A31/A55/A79 là vùng dự trữ lánh nạn, kỹ thuật và liên kết cứng. A32/A56/A80 có sảnh trên cao/phụ trợ và một lỗ mở local u=18..24, v=−8..8 m. Mỗi lỗ rộng 6×16=96 m². Cấu hình tầng lánh nạn và phân vùng cháy này mới là đề xuất không gian, chưa xác nhận theo quy chuẩn áp dụng.

## Lõi và văn phòng

| Đoạn | Vùng lõi local | Diện tích giữ chỗ |
| --- | --- | --- |
| A07–A30 | u=±17; v=±16 | 1.088 m² |
| A31–A54 | u=±15; v=±14 | 840 m² |
| A55–A78 | u=±14; v=±13 | 728 m² |
| A79–A98 | u=±12; v=±12 | 576 m² |

Các hình chữ nhật lồng nhau giúp duy trì phần lõi xuyên suốt. Việc giảm vùng lõi là giảm vùng bao kiến trúc; không có nghĩa được phép cắt bỏ tường chịu lực ở đúng cao độ đó mà không phân tích. Nhóm thang thấp kết thúc trước, phần thang cao và tuyến kỹ thuật tiếp tục trong vùng lõi trong. Chưa chốt số thang, tải trọng hoặc tốc độ.

Vành văn phòng thấp có chiều sâu danh nghĩa khoảng 17–18 m ở các trục chính. Cần nghiên cứu dầm/sàn và cột phụ; chưa cam kết một không gian không cột trên toàn bộ nhịp này. Vùng giữa ưu tiên mặt bằng chia 2–4 khách thuê; vùng cao có thể cho thuê toàn tầng. Diện tích net-lettable chưa được tính.

## Những giới hạn khi dựng

Giữ tâm đứng; không xoay loft; không đổi từng đoạn thành hộp giật cấp. Không khoét các rãnh thành khe xuyên qua toàn bộ tháp. Không thêm sân vườn toàn chu vi trên A chỉ vì ảnh phối cảnh có mảng xanh. Các khoảng thông tầng chỉ tồn tại khi có tọa độ trong JSON.
