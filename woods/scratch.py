import os
import re

directory = "/Users/artemmarkov/Desktop/🚀Разработка/imark.space/woods"

prices = {
    'I / I': {'7-8': ('61 078 ₽', '$719'), '10-11': ('56 682 ₽', '$667')},
    'I / II': {'7-8': ('46 968 ₽', '$553'), '10-11': ('44 496 ₽', '$523')},
    'II / II': {'7-8': ('45 114 ₽', '$531'), '10-11': ('43 260 ₽', '$509')},
    'II / III': {'7-8': ('41 200 ₽', '$485'), '10-11': ('39 140 ₽', '$460')},
    'II / IV': {'7-8': ('38 625 ₽', '$454'), '10-11': ('36 050 ₽', '$424')},
    'III / III': {'7-8': ('36 050 ₽', '$424'), '10-11': ('35 020 ₽', '$412')},
    'III / IV': {'7-8': ('35 020 ₽', '$412'), '10-11': ('33 990 ₽', '$400')},
    'IV / IV': {'7-8': ('31 684 ₽', '$373'), '10-11': ('30 012 ₽', '$353')},
    'ШОП': {'7-8': ('25 500 ₽', '$300'), '10-11': ('23 000 ₽', '$271')}
}

def make_td(rub, usd):
    return f'<td class="td-p"><span class="p-r">{rub}</span><span class="p-u">{usd}</span></td>'

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if filename != "index.html":
            # 1. Logo link
            content = re.sub(r'(<img class="hd-logo"[^>]*>)', r'<a href="index.html" style="display:block;">\1</a>', content)

            # 2. Reorder blocks (Extract Price Table and move after About)
            # Find the PRICE TABLE block
            price_match = re.search(r'(<!-- ═══════════ PRICE TABLE ═══════════ -->\s*<section.*?)(?=<!-- ═══════════|$)', content, flags=re.DOTALL)
            if price_match:
                price_block = price_match.group(1)
                
                # Add ID to the price table section
                price_block = re.sub(r'<section class="sec sec--dark">', r'<section class="sec sec--dark" id="price-table">', price_block)
                
                # Remove it from current location
                content = content.replace(price_match.group(1), '')
                
                # Find About block and append price block
                about_match = re.search(r'(<!-- ═══════════ ABOUT ═══════════ -->.*?)(?=<!-- ═══════════|<div class="divider">)', content, flags=re.DOTALL)
                
                if about_match:
                    about_block = about_match.group(1)
                    
                    # Add button to about block
                    btn_text = "Посмотреть прайс" if "_ru" in filename else "View Price List"
                    btn_html = f'\n    <div style="margin-top: 40px; text-align: center;">\n      <a href="#price-table" class="cta-btn">{btn_text}</a>\n    </div>\n  </div>\n</section>\n\n'
                    
                    new_about_block = re.sub(r'  </div>\n</section>\n?', btn_html, about_block)
                    
                    content = content.replace(about_block, new_about_block + price_block)

            # 3. Inject new columns into the table
            # Find thead row
            thead_match = re.search(r'<thead>\s*<tr>(.*?)</tr>\s*</thead>', content, flags=re.DOTALL)
            if thead_match:
                thead_inner = thead_match.group(1)
                # Split by th
                ths = re.findall(r'<th.*?>.*?</th>', thead_inner, flags=re.DOTALL)
                if len(ths) >= 5:
                    # Insert 7-8mm at index 5 (after 5-6mm which is index 4)
                    # wait: 0: Sort, 1: Application, 2: 3mm, 3: 4mm, 4: 5-6mm
                    if '7' not in ''.join(ths):
                        ths.insert(5, '<th>7–8 мм</th>')
                        ths.insert(7, '<th>10–11 мм</th>')
                        new_thead = '\n            '.join(ths)
                        content = content.replace(thead_inner, '\n            ' + new_thead + '\n          ')

            # Find tbody rows
            tbody_match = re.search(r'<tbody>(.*?)</tbody>', content, flags=re.DOTALL)
            if tbody_match:
                tbody_inner = tbody_match.group(1)
                rows = re.findall(r'<tr.*?>(.*?)</tr>', tbody_inner, flags=re.DOTALL)
                
                new_rows_html = []
                for row_inner in rows:
                    tds = re.findall(r'<td.*?>.*?</td>', row_inner, flags=re.DOTALL)
                    
                    # Identify the grade to get the right price
                    grade_match = re.search(r'<td class="td-g">(.*?)(?:<span|</td>)', tds[0])
                    if grade_match:
                        grade_text = grade_match.group(1).strip()
                        # normalize grade
                        grade = grade_text.replace(' / ', ' / ') # it's already clean
                        if grade in prices and len(tds) >= 5:
                            td_7_8 = make_td(prices[grade]['7-8'][0], prices[grade]['7-8'][1])
                            td_10_11 = make_td(prices[grade]['10-11'][0], prices[grade]['10-11'][1])
                            
                            # insert 7-8mm at index 5
                            if len(tds) == 9: # it was 9 columns originally, we make it 11
                                tds.insert(5, td_7_8)
                                tds.insert(7, td_10_11)
                                
                    new_rows_html.append('\n            ' + '\n            '.join(tds) + '\n          ')
                
                # Reconstruct tbody
                # Note we need the original <tr class="row-key"> wrappers
                # Let's replace the innerHTML of each tr
                for old_inner, new_inner in zip(rows, new_rows_html):
                    content = content.replace(old_inner, new_inner)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("HTML modifications complete.")
