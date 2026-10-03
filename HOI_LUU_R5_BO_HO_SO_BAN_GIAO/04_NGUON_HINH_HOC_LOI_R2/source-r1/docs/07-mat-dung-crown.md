# 07 · Mặt dựng, crown và giới hạn tạo hình

## Bề mặt A

Đường bao sàn là nguồn tạo hình. Nối các điểm cùng chỉ số giữa các cao độ; không đổi thứ tự đỉnh. Vỏ có bốn rãnh lõm nông, không xoắn. Tám gân chủ đạo nằm tại polar θ=22,5°+45°k và đi liên tục lên crown. OBJ dùng bán kính 0,45 m cho hình gân biểu đạt, tương đương bề rộng hình ảnh khoảng 0,9 m; đây không phải tiết diện cột chịu lực.

Nhịp mullion nghiên cứu: khoảng 160 đường đứng trên toàn chu vi A. Đây là hướng phát triển facade, chưa phải shop drawing; 256 điểm kiểm soát hình học không phải 256 panel kính. Khi chu vi giảm, bề rộng panel cũng giảm. Phải giải panelization thật, góc kính, khớp nối và khả năng dùng kính phẳng theo từng dải trước khi chốt số panel.

## Crown A

Chân crown nằm tại +452,40 m. Với θ là góc quanh tâm:

```text
Z_top(θ) = 478,50 + 1,50 cos(4θ)
u = tham số 0..1 từ mái tới vành trên
S(u) = 1 − 0,12 × (3u² − 2u³)
X,Y = tâm + S(u) × vector tới biên mái + (u³−2u²+u) × Hθ × T
Hθ = Z_top(θ) − Z_mái
T = vector độ dốc XY/Z từ vòng sàn cuối tới vòng mái, cùng chỉ số đỉnh
Z = 452,40 + u × [Z_top(θ) − 452,40]
```

Thành phần Hermite T nối hướng gân crown với độ dốc của đoạn thân cuối, tránh đổi hướng đột ngột ở chân crown. Vành trên dao động +477,00..480,00 m. Tám gân lớn tiếp tục từ thân; mô hình có thêm 32 gân nhỏ lấy mẫu từ chu vi và một vành liên tục. Gân nhỏ dùng bán kính biểu đạt 0,12 m; vành 0,18 m. Các kích thước này kiểm soát hình ảnh mô hình, chưa phải thiết kế cấu kiện. Đỉnh 480/285 m là giới hạn ngoài cùng: tiết diện gân/vành trong OBJ được cắt tại cao độ đó, không cộng thêm bán kính cấu kiện lên trên giới hạn.

Crown không có sàn thương mại. Mái +452,40 m là mặt kết thúc thể tích khai thác; khu kỹ thuật bên dưới thuộc A98. Chưa thêm sàn bảo trì riêng ở crown. Nếu cần sàn/bục bảo trì, phải bổ sung vào model và phân loại diện tích trước khi xuất bản tiếp.

## Bề mặt D và crown D

Gân D tiết chế hơn; mô hình dùng bán kính biểu đạt 0,24 m. Nhịp mullion nghiên cứu khoảng 128 đường đứng; kính sky lobby D35 lùi 3 m trong đoạn cao 6 m. Các gân ngoài không lùi theo kính.

```text
Z_top(θ) = 281,50 + 3,50 cos(θ)
S(u) = 1 − 0,035 × (3u² − 2u³)
Z = 269,45 + u × [Z_top(θ) − 269,45]
```

Tọa độ X/Y crown D dùng cùng hiệu chỉnh tiếp tuyến Hermite như A, với mái +269,45 m và tỷ lệ co 3,5%. Đỉnh thấp +278 m về phía −X, cao +285 m về phía +X. Crown là một vành nghiêng nhẹ, không thêm mũ nhọn. Giữ cùng vật liệu với A nhưng giảm tương phản và độ nổi gân.

## Vật liệu và ánh sáng

Kính màu trung tính, thanh kim loại bạc ấm, đá sáng ở chân công trình; các giá trị màu trong MTL chỉ phục vụ xem mô hình. Chưa chỉ định độ truyền sáng, phản xạ, SHGC hoặc một sản phẩm kính. Chọn kính và lam sau khi có hướng nắng thực.

Chiếu sáng ý tưởng tập trung vào sảnh, chân gân và crown; tránh dải sáng ngang ở mọi tầng vì sẽ làm mất cảm giác vươn đứng. Không coi một màn LED phủ toàn tháp là thành phần mặc định của thiết kế.

## Các lỗi hình khối cần loại khi kiểm tra bản dựng

- A thành nhiều hộp giật cấp hoặc xoay theo tầng.
- Crown đặt lên mái như một chiếc mũ không nối với gân thân.
- D cao gần bằng A hoặc được sao chép nguyên dáng A.
- Hai đế nhập thành một khối trên mặt đất; cầu nối trên cao giữa A/D.
- B/C bị đưa cùng về một phía của quảng trường, thay đổi footprint hoặc chiều cao.
- Tạo thêm tầng “ẩn” trong crown hoặc sky garden mà không cập nhật bảng diện tích.
- Nắn mặt dựng bằng modifier làm đường bao thay đổi nhưng bảng GFA giữ nguyên.
