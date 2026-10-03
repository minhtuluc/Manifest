# 09 · Kiểm tra, sai khác với ảnh và các bước còn lại

**Kết quả kiểm tra tự động: 350/350 điều kiện đạt.** Số này chỉ phản ánh các điều kiện hình học và số học được nêu dưới đây, không đo mức độ an toàn hoặc tính sẵn sàng thi công.

Mỗi tầng đã kiểm tra polygon hợp lệ, diện tích dương, lỗ mở nằm trong biên, lõi nằm trong biên và không chồng lỗ kiến trúc. Mỗi tháp đã kiểm tra ngân sách GFA, ngân sách đế, tính liên tục cao độ, bao hình giữa đế/thân và hình chiếu trong footprint tầng một.

| Kiểm tra | Kết quả | Chi tiết |
| --- | --- | --- |
| A_GFA | ĐẠT | 299999.99999999994 |
| A_pod_GFA | ĐẠT | 27999.999999999993 |
| A_podium_contains_body | ĐẠT | Outer envelopes only: reserved atria must be framed; no large unsupported tower overhang |
| A_projection_within_ground | ĐẠT | All floor projections inside ground envelope |
| A_vertical_continuity | ĐẠT | 452.39999999999935 |
| D_GFA | ĐẠT | 119999.99999999999 |
| D_pod_GFA | ĐẠT | 22000.0 |
| D_podium_contains_body | ĐẠT | Outer envelopes only: reserved atria must be framed; no large unsupported tower overhang |
| D_projection_within_ground | ĐẠT | All floor projections inside ground envelope |
| D_vertical_continuity | ĐẠT | 269.4500000000003 |
| A_in_site | ĐẠT | [14.0, 13.658387480858124, 100.0, 84.34161251914188] |
| D_in_site | ĐẠT | [193.0, 73.74200138785528, 271.0, 134.25799861214472] |
| B_in_site | ĐẠT | [87.0, 96.0, 162.0, 144.0] |
| C_in_site | ĐẠT | [128.0, 12.0, 205.0, 62.0] |
| pod_gap_AD | ĐẠT | {'clear_distance_m': 95.14814929090323} |
| pod_gap_AB | ĐẠT | {'clear_distance_m': 16.18666092199384} |
| pod_gap_AC | ĐẠT | {'clear_distance_m': 28.0} |
| pod_gap_DB | ĐẠT | {'clear_distance_m': 30.999999999999996} |
| pod_gap_DC | ĐẠT | {'clear_distance_m': 20.687343576793843} |
| pod_gap_BC | ĐẠT | {'clear_distance_m': 34.0} |
| mall_area | ĐẠT | 13999.999999999996 |
| mall_disconnected_BC | ĐẠT | BC footprint exclusion plus 6 m plan buffer |
| mall_connected | ĐẠT | Polygon |
| ramp_reserve_0 | ĐẠT | {'area': 1080.0, 'mall_overlap': 0.0} |
| ramp_reserve_1 | ĐẠT | {'area': 1080.0, 'mall_overlap': 0.0} |
| loading_in_mall_0 | ĐẠT | 240.0 |
| loading_in_mall_1 | ĐẠT | 204.0 |
| density | ĐẠT | {'footprint_including_400_allowance': 17756.0, 'ratio': 0.3883214871514489} |
| FAR_budget | ĐẠT | {'control_area': 631690.24, 'FAR_control': 13.814986112629851, 'headroom': 8459.76000000001} |
| BC_source | ĐẠT | {'units_per_tower': 92, 'units_both_towers': 184, 'residential_slab_area_per_tower': 54373.12, 'above_podium_slab_area_per_tower': 59845.12, 'crown_top': 158.7, 'common_per_level': 488, 'footprint': 1824} |

![E01 — Mặt đứng dùng cùng tỷ lệ X/Z; các đường tầng lấy từ CSV.](../drawings/E01-elevations.svg)

*E01 — Mặt đứng dùng cùng tỷ lệ X/Z; các đường tầng lấy từ CSV.*

![V01 — Khối 3D dựng bằng tọa độ; không dùng ảnh GenAI để nắn hình.](../drawings/V01-axonometric.svg)

*V01 — Khối 3D dựng bằng tọa độ; không dùng ảnh GenAI để nắn hình.*

## Khác biệt phải chấp nhận giữa bản dựng toán học và ảnh concept

1. B/C nằm hai phía tuyến quảng trường theo tọa độ đã giữ; một phối cảnh khiến chúng cùng nằm “phía sau” không được dùng đổi vị trí.
2. Tỷ lệ thân A trong R1 do 300.000 m² và 92 tầng thân quyết định. Muốn eo sâu hơn phải đổi profile và cân lại sàn, không bóp thân tùy mắt.
3. A có 27,60 m cao crown tối đa; D có 8,55–15,55 m. Các tấm ảnh mô tả crown lớn hơn hoặc thêm sàn kính trong crown không phải nguồn chuẩn.
4. Đế có sáu tầng với đường bao thật; các bậc vườn rộng mênh mông hoặc rất thấp trong ảnh có thể không đủ chứa 50.000 m².
5. Chưa có hình học cây xanh, mặt nước, sân chìm và nội thất hoàn chỉnh. Các chi tiết trang trí đó không được suy ra từ ảnh rồi tính như đã phối hợp với hầm.

## Việc nên làm ở R2

Ưu tiên đầu tiên là mặt bằng lõi và giao thông đứng A, vì chúng có thể thay đổi hiệu quả sàn lớn nhất. Đồng thời phát triển lưới cột xuống hầm và tuyến ram thật. Sau đó chọn module phòng khách sạn D và chốt ranh sảnh riêng trong đế.

Khi các phần trên ổn định, phát triển façade panelization, hình gân và crown bằng mặt cắt cấu tạo. Cuối cùng mới dựng phối cảnh vật liệu/cảnh quan từ model đã kiểm soát. Không dùng ảnh GenAI mới làm bước trung gian để quyết định tọa độ.
