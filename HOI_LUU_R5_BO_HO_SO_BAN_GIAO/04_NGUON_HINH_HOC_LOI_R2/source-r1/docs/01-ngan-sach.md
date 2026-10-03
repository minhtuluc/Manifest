# 01 · Ngân sách diện tích và cách đếm

| Thành phần | m² |
| --- | --- |
| Đất | 45.725,00 |
| Trần FAR | 640.150,00 |
| Thân A | 300.000,00 |
| Thân D — gói văn phòng | 70.000,00 |
| Thân D — gói khách sạn | 50.000,00 |
| Đế A | 28.000,00 |
| Đế D | 22.000,00 |
| Thân B/C, theo nguồn duplex R1 | 119.690,24 |
| Đế riêng B/C, ngân sách kế thừa | 28.000,00 |
| Mall B1, diện tích phân khu bảo thủ | 14.000,00 |
| Tổng diện tích kiểm soát | 631.690,24 |
| Biên còn lại | 8.459,76 |

**FAR kiểm soát = 13,81499.** Biên 8.459,76 m² tương đương khoảng 1,32% trần FAR; không nên dùng hết trước khi hoàn tất lõi và MEP.

## Ba trường diện tích phải phân biệt

- `envelope_area`: diện tích đa giác đường bao sàn tại cốt sàn.
- `void_area`: tổng lỗ mở kiến trúc hoặc vùng cắt khỏi sàn đã mô tả bằng hình học.
- `slab_area = envelope_area − void_area`: diện tích kiểm soát R1. Đây là quy ước sàn gộp kiến trúc; vẫn giữ diện tích lõi/giếng đứng chưa khai triển và các diện tích kỹ thuật, lánh nạn. Không phải diện tích bê tông đặt hàng, diện tích cho thuê hay kết quả tính FAR pháp lý.

Các tầng kỹ thuật, sảnh trên cao và tiện ích đã nằm trong gói 300.000/120.000 m². Không cộng thêm chúng sau khi chia GFA cho diện tích sàn điển hình. Các ban công/vườn trong đường bao đang được tính bảo thủ; việc được trừ hay phải tính sẽ phân loại ở bước pháp lý sau.

## Kiểm soát mật độ

Đế A 5.800 + đế D 4.500 + đế B 3.456 + đế C 3.600 = 17.356 m². Giữ thêm 400 m² cho công trình phụ, tổng 17.756,00 m², mật độ 38,83%. Còn 534 m² tới trần 18.290 m². Thân tháp và các tầng đế trên đã được kiểm tra nằm trong đường bao tầng một; không cộng trùng footprint thân vào footprint đế.

Khoản 400 m² là dự trù, chưa có hình học công trình phụ. Mái che lối vào, đầu ram, trạm kỹ thuật và phần nhô cần được thống kê ở lần sau. Diện tích trống còn lại không tự động là diện tích cây xanh: gồm quảng trường, đường xe, ram, mặt nước và các khoảng đệm.

## Tổng sàn hầm và tổng quy mô

Hầm theo đường bao 275×135 = 37.125 m² mỗi tầng; năm tầng là 185.625 m². Trong đó mall B1 14.000 m² đã nằm trong bảng FAR kiểm soát. Phần còn lại 171.625 m² là quỹ xe/kỹ thuật và giao thông, chưa phải sàn đỗ xe hữu dụng.

Diện tích trên mặt đất theo cùng quy ước là 617.690,24 m². Cộng toàn bộ đường bao hầm cho ra 803.315,24 m² quy mô hình học sơ bộ. Tổng này không phải BOQ bê tông và chưa trừ tất cả các lỗ ram, giếng kỹ thuật hay khoảng thông tầng hầm.
