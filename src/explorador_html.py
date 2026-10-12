"""Explorador del parlamento en HTML (una pantalla): hemiciclo filtrable, histórico y proyección, trends 6M/12M de envíos y EPOS
del EAN y de sus grupos, volúmenes y perfil político. Lee work/explorador.json (src/explorador_data.py).
Salida: reportes/EXPLORADOR_PARLAMENTO.html (abrir en el navegador) y work/explorador_artifact.html (sin el esqueleto <html>)."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ideo_brujulas6 as b6  # noqa

ROOT = Path(__file__).resolve().parents[1]; W = ROOT / "work"
OUT = ROOT / "reportes" / "EXPLORADOR_PARLAMENTO.html"


def main():
    D = json.loads((W / "explorador.json").read_text())
    D.update(colors=[b6.COL6[p] for p in D["parties"]], order=b6.ORDER6)
    tpl = (Path(__file__).parent / "explorador_template.html").read_text(encoding="utf-8")
    font = base64.b64encode((Path(__file__).parent / "fonts" / "inter-latin-opsz-normal.woff2").read_bytes()).decode()  # Inter (OFL), reserva de SF Pro fuera de Apple: sin internet
    page = tpl.replace("/*__FONT__*/", font).replace("/*__DATA__*/null", json.dumps(D, ensure_ascii=False, separators=(",", ":")))
    assert "/*__FONT__*/" not in page and "/*__DATA__*/" not in page
    (W / "explorador_artifact.html").write_text(page, encoding="utf-8")
    OUT.write_text("<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
                   f"</head><body>{page}</body></html>", encoding="utf-8")
    print(OUT, f"{OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
