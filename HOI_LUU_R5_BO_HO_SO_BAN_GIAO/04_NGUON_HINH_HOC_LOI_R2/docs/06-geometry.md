# 06 · Điều chỉnh hình học và B1
![P02](../drawings/P02-floor-envelope.svg)

Lỗ mở A32/A56/A80 đặt phía Đông trong R1 chồng lên tuyến E4 của bố trí mới. R2 chuyển chúng về phía +v (chưa phải Bắc địa lý), giữ mỗi lỗ **96 m²**: A32 u −8..8, v 18..24; A56/A80 u −8..8, v 17..23. A02 điều chỉnh hình lỗ/khuyết 1.950 m² để tránh lõi mới, giữ đúng diện tích khấu trừ và GFA tầng. Các thay đổi này có tọa độ trong JSON; OBJ R1 không phản ánh chúng.

![B02](../drawings/B02-mall-core-adjustment.svg)

Lõi xuyên B1 tăng A 1.088→1.512, D 624→1.024 m². Nếu chỉ trừ lõi mới khỏi mall cũ, diện tích còn **13.176 m²**, thiếu 824 m². R2 mở băng nối dưới quảng trường bằng phép giải diện tích, giữ hai anchor, quỹ ram và vùng riêng tư B/C. Tham số tạo băng tăng 24,60→44,36 m; nó không phải một hành lang mall thông thủy rộng 44 m. Mall thật còn bao gồm anchor, cửa hàng, khu BOH, lối đi và các lỗ lõi.

Mall B1 vẫn là một polygon liên thông **14.000 m²**; không chạm đế hoặc buffer riêng tư 6 m của B/C, không chồng quỹ ram. B1 còn lại 23.125 m² gồm đỗ xe, kỹ thuật và lõi. Quỹ mall đế A 21.000 + D 17.000 và B1 14.000 =52.000 m² gross vẫn được giữ **ở cấp budget**. R2 chưa chia cửa hàng và chưa chứng minh sảnh riêng lớn hơn vẫn nằm gọn trong 7.000/5.000 m² private của đế A/D; đó là điểm phải kiểm tra trước khi chốt mặt bằng mall.

B2–B5 mỗi tầng 37.125 m² vẫn chỉ để xe/kỹ thuật. Tổng 185.625 m² hầm không thay đổi. Quỹ ram 18×60 m ở R1 vẫn là vùng giữ chỗ, chưa có độ dốc hay bán kính quay thật. Chưa đưa ra số ô xe vì chưa có lưới cột, phòng máy, bể, đường chạy, phân khoang và hình học ram. Thang xe/mall được bố trí ngoài core thân và phải được bổ sung tọa độ/tải; không tính vào 77/23 thiết bị phía trên.

| Chỉ tiêu | R1 | R2 hiện tại | Sai khác |
| --- | --- | --- | --- |
| Proxy net văn phòng A | 184.799 | 156.719 | −28.080 m² |
| Proxy net văn phòng D | 44.261 | 34.901 | −9.360 m² |
| Mall B1 | 14.000 | 14.000 | 0 |
| Quỹ B1 còn lại | 23.125 | 23.125 | 0; gồm lõi và kỹ thuật |
| Tham số bề rộng tuyến mall | 24.60 m | 44.36 m | Mở băng dưới đất; quảng trường mặt đất vẫn theo R1 |
| GFA kiểm soát toàn khu | 631.690,24 | 631.690,24 | 0 |
| Dự phòng FAR | 8.459,76 | 8.459,76 | 0 |
