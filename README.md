# HỘI LƯU R5 — BỘ HỒ SƠ BÀN GIAO & CROWN MANIFEST

Bộ hồ sơ ngoại quan, khung hình học, công năng, kết cấu và dữ liệu kiểm soát dự án **HỘI LƯU R5** (kèm bản cập nhật **R6-CROWN**, snapshot 30/09/2026).

---

## 📁 Cấu trúc thư mục

```text
├── HOI_LUU_R5_BO_HO_SO_BAN_GIAO/
│   ├── 00_DOC_TRUOC.md              # Tài liệu hướng dẫn bắt buộc đọc trước khi đánh giá
│   ├── 01_HO_SO/                    # Hồ sơ bàn giao (.pdf / .md) & Catalog nguồn R1-R4
│   ├── 02_NGOAI_QUAN/               # HTML tương tác (AD_R3, BC_R4, CROWN_R6), bản vẽ SVG & scripts
│   ├── 03_DU_LIEU_KIEM_SOAT/        # Dữ liệu kiểm soát hình học (JSON & CSV xuất kèm)
│   ├── 04_NGUON_HINH_HOC_LOI_R2/    # Cơ sở lõi tháp, thang máy, hình học R2 và snapshot R1
│   ├── 05_DANH_GIA/                 # Biểu mẫu đánh giá độc lập & ma trận ràng buộc
│   ├── MANIFEST_SHA256.json         # Danh mục checksum SHA-256 toàn bộ 130 tệp tin
│   ├── PACKAGE_VALIDATION.json      # Kết quả kiểm định tính toàn vẹn và quy chuẩn gói
│   └── SOURCE_SNAPSHOT.json         # Metadata snapshot nguồn dữ liệu
│
└── danh_gia_crown/
    ├── ARCHIVE_R5_HOI_LUU_HO_SO_BAN_GIAO.pdf # Bản lưu trữ hồ sơ bàn giao R5
    ├── gen_crown_truoc_sau.py       # Script sinh sơ đồ so sánh hình học Crown
    ├── REV-C_crown_truoc_sau.png    # Ảnh đối chiếu Crown trước / sau (REV-C)
    └── REV-C_crown_truoc_sau.svg    # Vector đối chiếu Crown trước / sau (REV-C)
```

---

## 🚀 Điểm vào chính (Quick Start)

1. **Tổng quan & Điều kiện cần nắm**: Đọc [`HOI_LUU_R5_BO_HO_SO_BAN_GIAO/00_DOC_TRUOC.md`](HOI_LUU_R5_BO_HO_SO_BAN_GIAO/00_DOC_TRUOC.md).
2. **Hồ sơ thiết kế**: Mở [`HOI_LUU_R5_BO_HO_SO_BAN_GIAO/01_HO_SO/HOI_LUU_R5_HO_SO_BAN_GIAO.pdf`](HOI_LUU_R5_BO_HO_SO_BAN_GIAO/01_HO_SO/HOI_LUU_R5_HO_SO_BAN_GIAO.pdf).
3. **Mô hình ngoại quan trực quan**:
   - `CROWN_R6.html`: Ngoại quan đỉnh tháp & Crown R6.
   - `AD_R3.html`: Thân tháp A & D.
   - `BC_R4.html`: Thân tháp B & C.
   *(Các file HTML hoàn toàn tự chứa tài nguyên, có thể mở trực tiếp bằng trình duyệt mà không cần kết nối mạng).*
4. **Dữ liệu kiểm chuẩn**: Toàn bộ tham số và tọa độ được mô tả chi tiết trong thư mục `03_DU_LIEU_KIEM_SOAT/`.

---

## 🔒 Kiểm tra tính nguyên vẹn (Manifest Verification)

Kiểm tra tính toàn vẹn của toàn bộ tệp tin trong bộ hồ sơ bằng Python:

```bash
python -c "
import json, hashlib, os
manifest_path = 'HOI_LUU_R5_BO_HO_SO_BAN_GIAO/MANIFEST_SHA256.json'
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)
base_dir = os.path.dirname(manifest_path)
failed = 0
for item in manifest['files']:
    p = os.path.join(base_dir, item['path'])
    with open(p, 'rb') as fp:
        digest = hashlib.sha256(fp.read()).hexdigest()
    if digest != item['sha256']:
        print(f'MISMATCH: {item[\"path\"]}')
        failed += 1
if failed == 0:
    print(f'All {len(manifest[\"files\"])} files verified successfully against MANIFEST_SHA256.json.')
"
```
