# Dữ liệu kiểm soát - R5 snapshot + R6-CROWN

JSON là nguồn chính, CSV chỉ là export để đọc/đưa vào phần mềm. Đơn vị mét; X/Y local site; Z-up; chưa có hướng Bắc.

- `geometry-r2.json`: tất cả sàn A/D, đế, quảng trường, B1 và vùng dự trữ. `outer` và `core_geometry` là tọa độ thế giới. `core_local` dùng [x,y,w,h]; `core_local_R2_bounds` dùng [xmin,ymin,xmax,ymax]; cả hai đã cập nhật R2. Không nhầm hai cách mã hóa. Dùng `void_geometry` cho lỗ/khuyết thật, đặc biệt A02 có hình bất quy tắc; trường rectangle `voids_local` chỉ là mô tả rút gọn, không thay polygon lỗ R2.
- `r2-study.json`: nhóm thang, giả định thử, vị trí module, mô hình kiểm tra; không phải cấu hình mua.
- `duplex-source.json`: footprint local và các rect [x,y,w,h], cells phân căn, common, loggia, void, schedule40tầng. B: X94+u,Y102+v; C:X194−u,Y53−v. `area:null` ở năm tầng đế: chỉ có budget14.000/tháp, không tự chia đều hoặc thay bằng1.824.
- `facade-ad-r3.json`: lưới rings A/D dùng local centered u/v, Z; các góc/tiết diện concept. Nhịp D112thay128R1; crown D16phụ thay32R1. Planar-fit screen không là shop drawing. Các trường crown/gân cận đỉnh/ban đêm bị R6 thay, xem `supersedes`.
- `facade-bc-r4.json`: edge0..7 theo thứ tự đa giác; khoảng a/b đo dọc cạnh từ đỉnh đầu, không phải tọa độ thế giới; có lưới typical/penthouse, owners cho living/loggia. Type vision/owner null là mặt kính dự kiến chưa packing phòng. Trường `crown` và gân góc từ L36 bị R6 thay.
- `facade-crown-r6.json` (R6-CROWN): công thức crown A/D, đỉnh kiến trúc, gân hội tụ, nút lưới của fin, vùng chuyển A90–A98/D56–D62, crown khung mở B/C, dải kỹ thuật, chiếu sáng đêm, `supersedes`, `checks`, chỉ số R5/R6 và hash nguồn. Góc θ là polar local quanh tâm tháp, 0° = +X.
- `crown-R6-AD-surface.csv`: lưới bề mặt crown A/D, 25 bước u × nút panel (A160, D112), tọa độ thế giới. Đây là envelope tham chiếu, không phải một tấm vỏ kín: crown là khung gân/fin mở.
- `crown-R6-AD-members.csv`: polyline cấu kiện biểu đạt: `rib` (8/tháp), `fin` (A32, D23), `rim` (các đoạn vành, hở tại khe đỉnh). `source_panel_node` nối về nút lưới R3; điểm cuối của fin dừng trên gân nằm trên polyline gân tương ứng.
- Floor CSV A/D160 dòng; BC40 dòng chung cho cả hai tháp. CSV panel/outline giữ độ chính xác float; tên index_0based bắt đầu0. R3 rings gồm các sàn thân và vòng mái; nối đúng index. 256outline nodes không phải số panel.

Crown A/D từ R6 dùng công thức trong `facade-crown-r6.json`, vẫn giữ quy tắc tiếp tuyến Hermite R1 trên cùng chuỗi nút vòng mái R3. Công thức crown R1 trong `04_NGUON_HINH_HOC_LOI_R2/source-r1/docs/07-mat-dung-crown.md` chỉ còn giá trị lịch sử. D35 kính lùi3m cần offset riêng, không lấy nominal body quad thành IGU thực.

Trường `geometry-r2.json.towers.B/C` là reference khối; nội dung căn/void/loggia đầy đủ nằm ở duplex-source.json. OBJ R1 không phản ánh nội bộ R2, facade R3/R4 hoặc crown R6.
