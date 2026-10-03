# 05 · Cabin cần được kiểm tra bằng diện tích
Bài trình bày CIBSE của Richard Peters chỉ rõ số người hiệu dụng phải kiểm tra bằng diện tích cabin, không thể chỉ lấy kg chia khối lượng người rồi nhân 80%; ví dụ diện tích mỗi người 0,21 m² cho văn phòng và 0,30 m² cho khách sạn/nhà ở [4]. R2 dùng các giá trị đó để đặt **yêu cầu diện tích cabin**, không giả định cabin lớn chỉ vì tải trọng ghi lớn.

Diện tích thông thủy yêu cầu = P × diện tích/người ÷0,80. Tải khởi điểm dưới đây là mục để trao đổi hãng; chưa chọn một sản phẩm đáp ứng đồng thời tải, diện tích, tốc độ và travel.

| Nhóm | P hiệu dụng | Diện tích cabin thông thủy tối thiểu ở 80% tải diện tích | Quỹ ngoài tường / giếng | Tải khởi điểm nghiên cứu |
| --- | --- | --- | --- | --- |
| Local A | 22 (nhóm cuối thấp 20) | 5,78 m² (P20: 5,25) | 3,40 × 4,00 m | ~3.200 kg |
| Shuttle A | 33 | 8,67 m² | 4,00 × 4,20 m | ~5.000 kg; cần cabin cao tốc lớn |
| Văn phòng D | 26 | 6,83 m² | 3,40 × 3,80 m | ~4.000 kg |
| Khách sạn D | 16, có hành lý | 6,00 m² | 3,40 × 3,80 m | ~3.200 kg |


Quỹ module bao gồm dự trữ tường và không được sử dụng như clear shaft. Các mức tải/cabin này khá lớn, nhất là shuttle A 10 m/s. Nếu hãng không cung cấp được cabin phù hợp trong module, phải đổi số xe, P, tốc độ hoặc lõi và chạy lại số học. Không được giữ P33 rồi âm thầm thay bằng cabin thông thường nhỏ hơn. Những phép kiểm tra polygon ở đây không chứng minh khả năng lắp thiết bị.

Khuyến nghị bước tối ưu: thử DCS trên dân số đã khóa; so cấu hình double-deck với single-deck; so 35 s và 30 s; dùng cabin area thật. Double-deck có thể giảm số giếng nhưng cần trả lại diện tích cho sảnh hai cao độ và lối chuyển. Các cặp A31/32, 55/56, 79/80 đều cách 6 m, phù hợp để nghiên cứu, nhưng tầng dưới đang giữ cho kỹ thuật/outrigger; cần tách luồng và kiểm tra pit local trước khi chọn.
