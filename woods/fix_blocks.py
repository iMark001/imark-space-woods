import os
import re

directory = "/Users/artemmarkov/Desktop/🚀Разработка/imark.space/woods"

# --- 1. Add .bullet-list CSS to pages.css ---
css_path = os.path.join(directory, "pages.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

if ".bullet-list" not in css_content:
    bullet_css = """
/* ── BULLET LIST (Simplified Blocks) ── */
.bullet-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 12px; max-width: 860px; }
.bullet-list li {
  position: relative; padding-left: 24px; font-size: 14px; line-height: 1.6; color: var(--body2);
  background: var(--white); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 20px 16px 44px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.bullet-list li::before {
  content: '✓'; position: absolute; left: 16px; top: 16px; color: var(--amber); font-weight: bold; font-size: 14px;
}
.bullet-list strong { color: var(--light); font-weight: 600; }
"""
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(bullet_css)

# --- 2. Update HTML files ---
for filename in os.listdir(directory):
    if filename.endswith(".html") and filename != "index.html":
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # A. Move button from About to Hero
        # Find button in About
        btn_match = re.search(r'(\s*<div style="margin-top: 40px; text-align: center;">\s*<a href="#price-table" class="cta-btn">.*?</a>\s*</div>)', content)
        if btn_match:
            btn_html = btn_match.group(1)
            content = content.replace(btn_html, "") # remove from about
            
            # Change margin and insert into Hero
            hero_btn_html = btn_html.replace('margin-top: 40px; text-align: center;', 'margin-top: 32px;')
            # Insert after hero-pills closing div
            content = re.sub(r'(<div class="hero-pills">.*?</div>)', r'\1' + hero_btn_html, content, flags=re.DOTALL)

        # B. Replace Why-Grid and App-Grid in Construction files
        if filename == "construction_ru.html":
            why_ru = """<ul class="bullet-list">
      <li><strong>Берёза — лучший материал для опалубки:</strong> высокая плотность шпона, многоразовое использование, чистая поверхность бетона.</li>
      <li><strong>Для жилого строительства (Класс Е-0.5):</strong> вдвое ниже стандарта Е1. Безопасен для внутренней отделки.</li>
      <li><strong>Широкая линейка:</strong> тонкие (3–6 мм) — обшивка, средние (9–12 мм) — полы, толстые (14–30 мм) — опалубка.</li>
      <li><strong>Стабильное качество:</strong> контроль на всех этапах, отклонения строго в рамках ГОСТ.</li>
      <li><strong>Пакет документов для сдачи объекта:</strong> декларации и сертификаты для технадзора.</li>
      <li><strong>Прямая цена завода:</strong> отсутствие наценок посредников и экономия бюджета.</li>
    </ul>"""
            content = re.sub(r'<div class="why-grid">.*?</div>\s*</div>\s*</section>', why_ru + '\n  </div>\n</section>', content, flags=re.DOTALL)

            app_ru = """<ul class="bullet-list">
      <li><strong>🏢 Опалубка (Сорт III/III, III/IV · 18–21 мм):</strong> Дефекты не влияют на прочность. Обеспечивает минимальную усадку и чистую поверхность бетона.</li>
      <li><strong>🏠 Полы и покрытия (Сорт II/III, II/IV · 9–18 мм):</strong> Чистое лицо. Идеально под паркет, ламинат или сплошной настил.</li>
      <li><strong>🪟 Перегородки и стены (Сорт II/II, II/III · 4–12 мм):</strong> Ровные поверхности под покраску и финишную отделку.</li>
      <li><strong>📦 Кровля и временные сооружения (Сорт IV/IV, ШОП · 9–30 мм):</strong> Технический сорт по минимальной цене.</li>
    </ul>"""
            content = re.sub(r'<div class="app-grid">.*?</div>\s*</div>\s*</section>', app_ru + '\n  </div>\n</section>', content, flags=re.DOTALL)

        elif filename == "construction_en.html":
            why_en = """<ul class="bullet-list">
      <li><strong>Birch — the best for formwork:</strong> high density, multi-use, clean concrete surface.</li>
      <li><strong>For residential construction (Class E-0.5):</strong> half the E1 limit, safe for interior finishes.</li>
      <li><strong>Wide range:</strong> thin (3-6mm) for cladding, medium (9-12mm) for floors, thick (14-30mm) for formwork.</li>
      <li><strong>Consistent quality:</strong> strict quality control within GOST tolerances.</li>
      <li><strong>Full documentation:</strong> all certificates needed for technical supervision.</li>
      <li><strong>Direct factory price:</strong> no middleman markups, saving project budget.</li>
    </ul>"""
            content = re.sub(r'<div class="why-grid">.*?</div>\s*</div>\s*</section>', why_en + '\n  </div>\n</section>', content, flags=re.DOTALL)

            app_en = """<ul class="bullet-list">
      <li><strong>🏢 Formwork (Grade III/III, III/IV · 18–21 mm):</strong> Defects don't affect strength. Clean concrete surface.</li>
      <li><strong>🏠 Floors & Coverings (Grade II/III, II/IV · 9–18 mm):</strong> Clean face. Perfect for parquet, laminate or continuous flooring.</li>
      <li><strong>🪟 Partitions & Walls (Grade II/II, II/III · 4–12 mm):</strong> Even surfaces for painting and finishing.</li>
      <li><strong>📦 Roof Underlays & Temporary Structures (Grade IV/IV, SHOP · 9–30 mm):</strong> Technical grade at minimum price.</li>
    </ul>"""
            content = re.sub(r'<div class="app-grid">.*?</div>\s*</div>\s*</section>', app_en + '\n  </div>\n</section>', content, flags=re.DOTALL)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("Done")
