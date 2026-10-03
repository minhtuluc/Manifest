# 04 · Tháp D — văn phòng, khách sạn và sky lobby

**62 tầng vật lý = 6 tầng đế + 56 tầng thân.** D07–D34 là gói văn phòng 70.000 m²; D35–D62 là gói khách sạn 50.000 m². Tổng thân 120.000 m², chưa bao gồm 22.000 m² đế. Trong từng gói đã có sảnh, lõi, kỹ thuật và lánh nạn.

## Profile theo công năng

Đoạn văn phòng: t=(z−34)/(157,45−34), q=t^2.103257151817; W=60−4q, H=48−12q, R=12−2q.

Đoạn khách sạn: t=(z−157,45)/(269,45−157,45), q=t^1.071919145920; W=56−6q, H=36−2q, R=10−q.

Mỗi đoạn dùng hình chữ nhật bo góc, 256 điểm theo chu vi, cùng tâm (238;104). Hai profile gặp nhau ở 56×36 m, R=10 m tại +157,45 m: không có bước nhảy kích thước ở ranh công năng. Đạo hàm đường bao có thể đổi ở đây; vùng sky lobby và các gân đứng xử lý chuyển tiếp. Không dùng smooth modifier làm thay đổi biên sàn đã tính.

| Tầng | Z m | Cao tầng m | W m | H m | Sàn m² | Công năng |
| --- | --- | --- | --- | --- | --- | --- |
| D07 | 34,00 | 5,60 | 60,00 | 48,00 | 2.756,09 | Office |
| D20 | 90,60 | 5,60 | 59,22 | 45,67 | 2.588,89 | MEP/refuge reservation |
| D21 | 96,20 | 4,25 | 59,05 | 45,16 | 2.492,64 | Office |
| D34 | 151,45 | 6,00 | 56,40 | 37,19 | 2.008,14 | MEP/refuge reservation |
| D35 | 157,45 | 6,00 | 56,00 | 36,00 | 1.929,94 | Hotel sky lobby |
| D36 | 163,45 | 3,80 | 55,74 | 35,91 | 1.836,47 | Hotel |
| D48 | 209,05 | 5,20 | 53,39 | 35,13 | 1.796,63 | MEP/refuge reservation |
| D62 | 263,65 | 5,80 | 50,33 | 34,11 | 1.646,30 | MEP/refuge reservation |

![D01 — Đường bao D và vùng lõi; D35 có vùng kính lùi 3 m.](../drawings/D01-plans.svg)

*D01 — Đường bao D và vùng lõi; D35 có vùng kính lùi 3 m.*

## Cao độ và khoảng lùi

Đế kết thúc +34,00 m. Văn phòng điển hình 4,25 m; D07/D20 cao 5,60 m, D34 cao 6,00 m. Khách sạn điển hình 3,80 m; D35 cao 6,00 m, D48 cao 5,20 m, D62 cao 5,80 m. Mái +269,45 m, crown cao từ +278,00 đến +285,00 m.

Sky lobby bắt đầu D35, +157,45 m. Từ +157,45 đến +163,45 m, kính lùi vào 3 m so với đường bao sàn bằng phép offset polygon. Gân ngoài tiếp tục theo biên thân. Vùng vành sàn ngoài kính là sân vườn/hiên có mái ở mức concept; được giữ trong diện tích kiểm soát bảo thủ. Không cộng thêm diện tích sky garden ngoài 120.000 m².

D21 có lỗ mở 5×12=60 m² tại u=18..23, v=−6..6. D36 có lỗ mở 5×16=80 m² tại u=16..21, v=−8..8; liên hệ với sảnh dưới. Chưa đặt bể bơi hay ballroom trên cao vì chúng sẽ thay đổi tải trọng và tổ chức kỹ thuật.

## Lõi và các luồng riêng

Vùng lõi văn phòng: 26×24=624 m², tâm tại tâm tháp. Vùng lõi khách sạn: 24×16=384 m², lồng trong lõi dưới. Hệ express khách sạn và hệ phục vụ phải đi xuyên vùng lõi dưới; khoảng 240 m² chênh lệch chỉ là quỹ cho tổ chức thang văn phòng, sảnh và kỹ thuật, không phải diện tích tự do chắc chắn.

| Luồng | Tuyến bắt buộc |
| --- | --- |
| Nhân viên/khách văn phòng | Sảnh văn phòng → kiểm soát → thang văn phòng |
| Khách khách sạn | Drop-off riêng → sảnh dưới → express → sky lobby → thang phòng |
| Nhân viên và hàng khách sạn | BOH B1/đế → thang phục vụ → kho tầng/bếp/housekeeping |
| Khách mall | A/B1/D → thang cuốn thương mại; không dùng thang khách sạn làm tuyến xuyên |

Số phòng chưa chốt. Cần chọn module phòng, tỷ lệ suite, diện tích nhà hàng/club/housekeeping và mô phỏng thang trước khi suy ra số keys. Vành khách sạn tại phần thấp có chiều sâu trục ngắn khoảng (36−16)/2=10 m, bao gồm cả phần hành lang/tường khi phát triển mặt bằng.
