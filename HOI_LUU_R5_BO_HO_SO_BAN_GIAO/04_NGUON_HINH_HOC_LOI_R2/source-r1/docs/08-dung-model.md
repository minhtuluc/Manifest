# 08 · Dựng mô hình và quản lý thay đổi

## Các file dùng trực tiếp

| File | Mục đích |
| --- | --- |
| `data/geometry.json` | Nguồn tọa độ, cao độ, polygon, vùng lõi và diện tích |
| `data/floor-schedule.csv` | 160 dòng tầng A/D; mỗi dòng có diện tích bao/lỗ/sàn |
| `data/outline-vertices.csv` | 256 điểm cho mỗi tầng A/D, tọa độ thế giới |
| `data/bc-source-r1.json` | Dữ liệu duplex B/C kế thừa, không chỉnh sửa |
| `model/hoi-luu-r1.obj` + `.mtl` | Khối vỏ, đế, gân/crown và B/C tham chiếu, đơn vị mét |
| `scripts/import_blender.py` | Dựng scene Blender từ OBJ bằng bộ đọc đơn giản, không phụ thuộc addon nhập OBJ |
| `drawings/*.svg` | Bản vẽ kiểm soát vector, có thể phóng lớn |
| `scripts/build_geometry.py` | Giải profile và tái sinh dữ liệu/bảng kiểm tra |
| `scripts/build_views.py` | Sinh lại bản vẽ và mô hình |

## Thứ tự dựng

1. Đặt đơn vị mét, Z hướng lên; nhập biên đất 295×155 m và năm cốt hầm.
2. Nhập B/C làm reference khóa; không scale theo ảnh.
3. Dựng đế A/D từng tầng theo polygon; sử dụng `void_geometry` để cắt sàn khi cần dựng slab thật.
4. Dựng vòng biên thân theo từng tầng; nối chỉ số đỉnh tương ứng. Cả A/D không xoay trục.
5. Dựng lõi theo các vùng giữ chỗ; không nhầm vùng lõi với mặt bằng thang đã thiết kế.
6. Dựng vùng kính lùi D35. Giữ sàn và gân ngoài theo biên gốc.
7. Dựng crown theo công thức riêng, không kéo dài nguyên khối kính lên tới đỉnh.
8. Thêm mullion, vật liệu, cảnh quan và nội thất sau khi đã đối chiếu silhouette và GFA.

OBJ là mô hình kiểm soát bề mặt, không có toàn bộ sàn đặc, tường ngăn, cửa, thiết bị, móng, ram đã giải dốc hay căn hộ chi tiết. Một số mặt trên/dưới không được đóng để tiện kiểm tra loft; không dùng tính thể tích bê tông từ OBJ. Floor plate/void thật nằm trong JSON.

## Trong Blender

Giải nén toàn bộ thư mục. Mở `scripts/import_blender.py` trong Text Editor và Run Script. Nếu Blender không tìm được đường dẫn script qua `__file__`, sửa biến `PACKAGE` thành đường dẫn thư mục `hoi-luu-r1`. Script tạo collection riêng `HOI_LUU_R1`, không xóa scene hiện có; đặt unit scale 1 m và vật liệu cơ bản. Nếu collection cùng tên đã có, script tạo hậu tố phiên bản mới.

Script import đã được kiểm tra cú pháp và đối chiếu định dạng OBJ; chưa chạy trong một phiên Blender của dự án này. Model OBJ dùng đỉnh/quads tiêu chuẩn và có thể nhập trực tiếp qua trình nhập OBJ của phần mềm khác, lưu ý lựa chọn trục Z-up.

## Tái tạo toàn bộ bộ hồ sơ

Python 3 cần `numpy`, `shapely`, `matplotlib`, `markdown`. Trong thư mục gói chạy lần lượt:

```bash
python scripts/build_geometry.py
python scripts/build_views.py
python scripts/build_report.py
```

`bc-source-r1.json` đã kèm trong gói nên không cần truy cập file HTML nguồn ở ngoài. Không đổi N=256 hoặc điểm bắt đầu chu vi riêng cho một tầng. CSV được làm tròn khi ghi đỉnh tới 6 chữ số thập phân; JSON giữ độ chính xác tính toán.

## Dung sai và thay đổi

Mục tiêu đối chiếu tọa độ 0,01 m, cao độ 0,01 m; tổng diện tích khi tái tính từ JSON sai khác dưới 0,10 m². Nếu tái dựng bằng NURBS/arc thật thay cho đa giác 256 điểm, sẽ có chênh diện tích nhỏ; phải báo cáo chênh và thống nhất lại diện tích, không ghi là khớp tuyệt đối.

Mỗi thay đổi tâm, W/H/R, số tầng, cao tầng, lỗ mở, core hoặc crown phải tăng revision, chạy lại kiểm tra, tái xuất CSV/SVG/OBJ. Thay đổi vật liệu hay camera không làm đổi revision hình học nếu tọa độ không đổi. Không ghi đè R1 khi phát triển R2.
