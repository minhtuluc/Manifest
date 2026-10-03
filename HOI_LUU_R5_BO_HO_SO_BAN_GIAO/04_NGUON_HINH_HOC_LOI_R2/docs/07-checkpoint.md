# 07 · Checkpoint và bước phát triển tiếp
**3035/3035 điều kiện hình học/số học đạt** trong bản chạy này. Trong số đó có nhiều phép so chồng từng cặp module; số lượng lớn không có nghĩa hồ sơ đã gần thi công. Kiểm tra gồm lõi/lỗ mở trong biên từng tầng, bảo toàn GFA, module không chồng nhau, phần giếng còn hoạt động nằm trong lõi đúng đoạn, nối đầu giếng/pit theo giả định, B1 giữ diện tích/độ liên thông và 17 nhóm thang vượt phép sàng lọc cơ sở.

Không có kiểm tra: wall/core structural analysis, cabin CAD, fire/smoke compartment, travel-distance evacuation, manufacturer dispatch simulation, shaft clearances under drift, hotel room packing, detailed parking/ramp, operational resilience. Cụm “screen_pass” trong JSON chỉ chỉ điều kiện RTT/HC và interval của giả định tương ứng.

**Quyết định kiến trúc t đề xuất:** giữ vỏ R1 và dùng R2 này làm biên không gian để kiểm tra tiếp, chưa khóa lõi 1.512/1.024 m² như thiết kế tối ưu. Ưu tiên giải hai nhóm thấp A trước; song song lấy cabin/shaft/headroom từ hãng để so single-deck/DCS/double-deck. Chỉ sau đó khóa lõi, lập mặt bằng phòng D và phân chia mall. Mức net thất thoát hiện tại đủ lớn để yêu cầu tối ưu kỹ thuật trước khi phát triển nội thất hoặc phối cảnh.

| Gói việc tiếp | Sản phẩm cần ra |
| --- | --- |
| Tối ưu A | So số giếng, net floor, thời gian hành trình tổng và một xe hỏng; giải Z1 trước |
| Phối hợp hãng | Cabin area, tải, shaft clear, pit, overhead, machine space, travel từng nhóm |
| Lõi/kết cấu/PCCC | Tường và dầm thật, lobbies có bảo vệ, cầu thang/chiều rộng/lánh nạn phù hợp hồ sơ địa điểm |
| D phòng + vận hành | Module phòng trong biên thật; xác nhận keys, BOH, lounge, mixed hotel traffic |
| Hầm + đế | Lưới cột, ram thật, core/mall/parking lifts, private lobbies và cửa hàng trong gross budget |

## Tài liệu và cách dùng
`HOI_LUU_R2.html` chứa toàn bộ báo cáo/bản vẽ, đọc độc lập. `data/geometry-r2.json` là nguồn polygon/cao độ; `data/r2-study.json` chứa giả định, 17 nhóm, module và kiểm tra; hai CSV dùng trao đổi số liệu. Các SVG zoom không vỡ. `scripts/build_r2.py` và `build_drawings_report.py` tái tạo bộ này từ nguồn R1; không cần ảnh GenAI.

## Nguồn tham khảo kỹ thuật
1. [ISO 8100-32:2020 — phạm vi lập kế hoạch và chọn thang](https://www.iso.org/standard/73084.html). Chỉ sử dụng trang mô tả phạm vi; chưa tuyên bố tuân thủ toàn văn.
2. [CIBSE Guide D3 — Lift traffic design using calculation, 2025](https://www.cibse.org/knowledge-research/knowledge-portal/guide-d3-lift-traffic-design-using-calculation-2025/).
3. [CIBSE Guide D4 — Lift traffic design using simulation, 2025](https://www.cibse.org/knowledge-research/knowledge-portal/guide-d4-lift-traffic-design-using-simulation-2025/).
4. [Richard Peters / CIBSE — 80% Lift Traffic Design’s Most Misunderstood Number, 12/11/2025](https://www.cibse.org/media/x0sfnskv/80-lift-traffic-design-s-most-misunderstood-number-cibse.pdf). Tham chiếu điều kiện sức chứa theo diện tích cabin.
5. [KONE — Elevator planning handbook for architects](https://www.kone.com/en/Images/8559_Global_EN_Elevator_Planning_Handbook_tcm17-75237.pdf). Tham chiếu quy trình phối hợp early planning, shaft và overhead; không dùng để xác nhận sản phẩm cho R2.

Đây là nghiên cứu kiến trúc do trợ lý xây dựng theo hướng ưu tiên hình học/kết cấu; không phải tài liệu do SOM phát hành hoặc kiểm duyệt.
