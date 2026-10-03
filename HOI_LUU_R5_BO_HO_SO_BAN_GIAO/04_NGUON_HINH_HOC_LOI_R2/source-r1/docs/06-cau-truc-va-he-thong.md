# 06 · Khung kết cấu, lõi và hệ thống cần phối hợp

## Mức độ của tài liệu

Phần này xác định đường truyền lực và không gian cần giữ để kiến trúc không tự mâu thuẫn. Chưa có tải trọng tính toán, kích thước cột/tường được kiểm chứng, lượng thép, móng, chuyển vị, gia tốc gió hoặc phân tích động đất. Các gân trong OBJ là hình học biểu đạt kiến trúc; không được lấy tiết diện gân làm tiết diện cột.

## Tháp A

Hệ nghiên cứu: lõi trung tâm kết hợp cột lớn ở biên, cột phụ chịu tải đứng và các tầng liên kết cứng. Tám đường gân lớn định hướng tại góc polar 22,5°+45°k; đường tâm kết cấu dự kiến lùi vào mặt dựng, phải được chọn lại cùng lưới cột thực. Lõi không nghiêng; đường biên và cột biên có thể nghiêng theo profile.

Tuyến tải đứng: sàn → dầm/sàn chịu lực → cột/lõi → đài/móng. Tuyến tải ngang nghiên cứu: mặt dựng/sàn diaphragm → lõi và hệ biên → liên kết cứng → móng. Độ cong của vỏ ngoài chưa chứng minh bất kỳ mức tiết kiệm vật liệu nào.

Các cụm A31–A32, A55–A56, A79–A80 là quỹ không gian để phối hợp outrigger/belt, MEP và sky lobby. Cần phân chia rõ vùng dầm/giằng với vùng khách sử dụng; không bố trí giằng chéo xuyên một sảnh đang được mô tả là không gian trống. A98 giữ cho kỹ thuật mái và chân crown.

Vành sàn thấp có nhịp lớn. Phải nghiên cứu cột phụ hoặc hệ dầm phù hợp thay vì tự coi toàn bộ khoảng lõi–biên là sàn phẳng không cột. Khoảng bo góc và rãnh lõm không được làm cột đổi hướng đột ngột giữa hai tầng.

## Tháp D

Hệ nghiên cứu: lõi trung tâm, cột biên và sàn; vùng chuyển công năng tại D34–D35 được giữ để giải quyết chênh chiều sâu mặt bằng, kỹ thuật khách sạn và cấu tạo sky lobby. Lõi khách sạn lồng trong vùng lõi văn phòng. Cột chính cần tiếp tục qua tầng kính lùi; vườn trên cao không tạo ra một tầng “mềm” do xóa bỏ cột.

Không mặc định D cần cùng một hệ outrigger như A. Việc dùng hay bỏ hệ này phụ thuộc phân tích tải ngang, chiều cao, độ cứng và tiện nghi.

## Tiếp đất và hầm chung

Các lõi A/D đi xuyên đế xuống hầm. Tám tuyến gân chỉ là gợi ý vị trí cột lớn; khi xác lập lưới cột thật, phải đặt nó vào bản vẽ B1–B5 trước khi chia ô xe. Tránh đặt atrium, ballroom hoặc ram tại vùng đài và cột lớn. Trường hợp bắt buộc có chuyển tải phải được đánh dấu thành một quyết định riêng với hệ quả chiều cao và chi phí.

Phương án móng có thể gồm móng bè kết hợp cọc, nhưng chưa được chọn. Không xác định đường kính/chiều dài cọc hoặc chiều dày bè khi chưa có khảo sát. Độ lún chênh A–D–B/C và tương tác với hầm chung là mục kiểm tra bắt buộc. Khe nhiệt, khe lún và giải pháp chống thấm xuyên khe chưa được định vị.

## Giao thông đứng và MEP

Lõi A cần mô phỏng theo dân số văn phòng, diện tích sử dụng, giờ cao điểm và chiến lược sky lobby. Lõi D phải đồng thời phục vụ khách, nhân viên, hàng, rác và cứu hỏa mà không trộn luồng mall với khách sạn. Không suy ra số thang chỉ bằng số tầng.

Các vùng kỹ thuật/lánh nạn trong CSV là diện tích có thật đã tính vào quỹ sàn. Công suất cấp điện, máy phát, làm mát, bơm, bể nước và hút khói chưa tính. B1 không được biến phần mall thành chỗ đặt máy sau khi đã ký ngân sách thương mại; nếu cần thay đổi phải cập nhật diện tích.

Phần tầng hầm không bao gồm diện tích được tự động coi là phòng máy dưới móng. Vị trí bể, hố pit, trạm biến áp, đường vận chuyển thiết bị và khu rác phải được bổ sung bằng polygon và cao độ cụ thể.

## Các kiểm tra chuyên ngành trước khi nâng mức hồ sơ

1. Khảo sát địa chất, mực nước, hố đào và ảnh hưởng công trình lân cận.
2. Phân tích kết cấu và biến dạng dài hạn; kiểm tra co ngắn chênh cột/lõi và dung sai mặt dựng.
3. Thí nghiệm/đánh giá gió cho tải trọng, tiện nghi tháp và gió ở quảng trường.
4. Phân khoang, thoát nạn, tầng lánh nạn, thang chữa cháy và tiếp cận xe cứu hỏa theo hồ sơ địa điểm.
5. Mô phỏng giao thông đứng và kiểm tra vận hành khách sạn.
6. Chốt công suất MEP, tải trọng kỹ thuật và chỗ tiếp cận bảo trì.

Đây là danh mục công việc còn thiếu, không phải tuyên bố R1 đã đạt các kiểm tra trên.
