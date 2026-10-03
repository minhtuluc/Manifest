# HỘI LƯU R5 - đọc trước khi đánh giá

Bộ hồ sơ ngoại quan và khung hình học/công năng/kết cấu để đánh giá độc lập. Snapshot 30/09/2026. R5 tổng hợp R1–R4 và không đổi hình học. **R6-CROWN** (REV-C01…C08, chủ đầu tư chỉ đạo) sửa crown, vùng chuyển cận đỉnh, dải kỹ thuật và chiếu sáng đêm, đồng thời nâng đỉnh kiến trúc: A +519,54 m (envelope +520), D +309,96 m (envelope +310), B/C +159,90 m (giữ H02). Sàn, mái, lõi và GFA không đổi. Chưa ghi nhận phê duyệt cuối. Tên file giữ tiền tố R5 để không gãy liên kết.

## Điểm vào

1. Đọc `01_HO_SO/HOI_LUU_R5_HO_SO_BAN_GIAO.pdf` (hoặc bản Markdown cùng tên). Hồ sơ truyền đạt vision, số liệu, trạng thái quyết định, các giao diện và việc cần phản biện.
2. Mở `02_NGOAI_QUAN/CROWN_R6.html` để xem crown R6 (7 bản vẽ, bảng R5/R6, JSON nhúng), rồi `AD_R3.html` và `BC_R4.html` cho thân tháp, biến thể và dữ liệu nhúng. Mỗi HTML tự chứa nội dung, không cần mạng để xem. Có thể tái tạo toàn bộ dữ liệu và bản vẽ R6 bằng lệnh `python 02_NGOAI_QUAN/scripts/build_crown_r6.py` (chỉ dùng thư viện chuẩn).
3. Dựng/đo bằng `03_DU_LIEU_KIEM_SOAT/*.json` và CSV xuất kèm. Có bản vẽ SVG phóng lớn tại `02_NGOAI_QUAN/drawings/`.
4. Tra cấu hình lõi/thang và toàn bộ cơ sở trong `04_NGUON_HINH_HOC_LOI_R2/`.
5. Trả nhận xét theo biểu mẫu ở `05_DANH_GIA/`, kèm ID thay đổi và bảng tác động trước/sau.

## Những điều phải hiểu đúng

- A/D M2 và B/C K2 là phương án tham chiếu đề xuất, chưa được coi là duyệt cuối.
- Gân đứng là vỏ biểu đạt kiến trúc; chưa chứng minh là megacolumn. Không dùng kích thước gân làm tiết diện chịu lực.
- Lõi/thang R2 là cấu hình tính thử cần tối ưu; A thấp có dự phòng ít. 77/23 là bộ thang thử A/D, không phải giếng xuyên suốt hoặc danh mục mua.
- B/C giữ 92 duplex/tháp, 40 tầng, mái 154,2 m; đỉnh R6 159,9 m (R4 158,7 m), trong giới hạn H02 160 m; loggia có sàn cả hai tầng. Nhịp 7,2 m không là chiều cao thông thủy.
- R2 chỉ sửa lõi/lỗ/mall. R3 sửa ngoại quan A/D, D112panel và16gân phụ crown thay các ý tưởng R1. R4 sửa ngoại quan B/C. R6 chỉ thay crown/đỉnh, gân cận đỉnh, dải kỹ thuật và chiếu sáng; các trường bị thay được liệt kê trong `facade-crown-r6.json → supersedes`. Không dùng revision mới để ghi đè toàn bộ nền cũ.
- Crown R6 không có sàn khai thác. Chiều cao không khai thác tăng lên 73,9 m ở A (14,2%) và 46,3 m ở D (14,9%) là đánh đổi có chủ đích. Khung thép, gió, BMU và tĩnh không hàng không của crown R6 còn mở.
- `04_NGUON_HINH_HOC_LOI_R2/source-r1/model/*.obj` là khối tham chiếu R1 cũ, không phản ánh lõi/lỗ R2 hoặc mặt dựng R3/R4. Không có BIM facade hoặc model nội bộ R2 hoàn chỉnh đã phát hành.
- Không đo từ ảnh; ưu tiên tọa độ. Không có hướng Bắc, địa điểm, địa chất hoặc xác nhận pháp lý. Chưa có số ô xe, hệ chịu lực, công suất MEP hay keys khách sạn được packing chứng minh.
- Native scripts trong các nguồn gốc được lưu để truy nguyên, có thể chứa đường dẫn/dependencies của phiên tạo hồ sơ. Không được coi là gói BIM hoặc pipeline chạy ngay trên mọi máy. Dữ liệu JSON/CSV độc lập là nền trao đổi.

## Thứ tự xử lý sai khác

Đầu bài người dùng → R2 cho phần đã sửa → R1/duplex cho phần giữ → R6 cho crown/đỉnh/cận đỉnh → R3 cho facade A/D → R4 cho facade B/C → bản vẽ/báo cáo/model biểu đạt. Khi bản tóm tắt làm tròn, dùng số đầy đủ trong JSON.

Trạng thái H: giới hạn đầu bài. B: cơ sở so sánh hiện tại. P: đề xuất mặt dựng. O: còn mở. Thay B/P được đề nghị nhưng phải báo tác động; đổi H cần quyết định của chủ đầu tư.

## Kiểm tra nguyên vẹn

`MANIFEST_SHA256.json` ghi kích thước/hash các thành phần (không tự chứa hash của chính manifest). `PACKAGE_VALIDATION.json` ghi kết quả kiểm tra dữ liệu và đóng gói. PDF có trang đứng cho nội dung, trang ngang cho bản vẽ; SVG gốc để phóng lớn hoặc in riêng.
