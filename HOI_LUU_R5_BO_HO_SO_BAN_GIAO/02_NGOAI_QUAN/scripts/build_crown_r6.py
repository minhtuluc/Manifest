"""Rebuild all R6-CROWN outputs: control data (03_DU_LIEU_KIEM_SOAT), drawings (02_NGOAI_QUAN/drawings/CROWN_R6)
and the self-contained viewer 02_NGOAI_QUAN/CROWN_R6.html.

Usage:  python build_crown_r6.py      (Python 3.8+, standard library only)
"""
import json
import r6_export
import r6_figures
import r6_html

if __name__ == "__main__":
    data = r6_export.export()
    files = r6_figures.build_all()
    page = r6_html.build()
    print(json.dumps({"checks": {c["name"]: c["passed"] for c in data["checks"]}, "drawings": files, "html": page},
                     ensure_ascii=False, indent=1))
