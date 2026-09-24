#!/usr/bin/env python3
"""Собирает index.html из items.json. Запуск: python3 render.py"""
import json, time, datetime, urllib.request, urllib.error

BASE = "https://barus.skalkindmitriy.ru"
HEAD = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Каталог оборудования: недостающие данные и вопросы</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Russo+One&family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
<style>
body{margin:0;background:#f4f6f8;font:15px/1.6 Montserrat,Tahoma,sans-serif;color:#232323}
.wrap{max-width:1100px;margin:0 auto;padding:32px 40px 64px;background:#fff}
h1{font-family:'Russo One',Montserrat,sans-serif;font-weight:400;font-size:28px;border-bottom:3px solid #42c1c7;padding-bottom:12px;margin:0 0 8px}
.lead{margin:0 0 4px}.upd{color:#5b6570;font-size:13px;margin:0 0 20px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:#232323;color:#fff;text-align:left;padding:9px 10px;font-weight:600}
th:nth-child(1){width:3%}th:nth-child(2){width:11%}th:nth-child(3){width:12%}th:nth-child(4){width:10%}th:nth-child(5){width:15%}th:nth-child(7){width:10%}
a{color:#0e6d73}
td{padding:8px 10px;border-bottom:1px solid #e3e7ec;vertical-align:top}
tr:nth-child(even) td{background:#f7f9fb}
td ul{margin:4px 0 0;padding-left:18px}li{margin:2px 0}
.st{font-weight:600}.open{color:#b3541e}.done{color:#0e6d73}
@media(max-width:700px){
.wrap{padding:20px 16px 40px}h1{font-size:22px}
thead{display:none}
table,tbody,tr,td{display:block;width:auto}
tr{border:1px solid #e3e7ec;border-radius:6px;margin:0 0 14px;padding:6px 12px}
tr:nth-child(even) td{background:none}
td{border:0;padding:4px 0}
td:nth-child(1){font-weight:600;color:#0e6d73}
td:nth-child(1)::before{content:"№ "}
td:nth-child(n+2)::before{display:block;font-size:12px;color:#5b6570;font-weight:600}
td:nth-child(2)::before{content:"Категория"}
td:nth-child(3)::before{content:"Подкатегория"}
td:nth-child(4)::before{content:"Серия"}
td:nth-child(5)::before{content:"Товар и артикулы"}
td:nth-child(6)::before{content:"Что не так"}
td:nth-child(7)::before{content:"Статус"}
td:empty{display:none}
}
@media print{body{background:#fff}.wrap{padding:0}tr{break-inside:avoid}}
</style></head><body><div class="wrap">
<h1>Каталог оборудования: недостающие данные и вопросы</h1>
<p class="lead">Что нужно дополнить или проверить в таблице оборудования, чтобы карточки на сайте были полными.</p>
'''
COLS = "<thead><tr><th>№</th><th>Категория</th><th>Подкатегория</th><th>Серия</th><th>Товар и артикулы</th><th>Что не так</th><th>Статус</th></tr></thead>"

_checked = {}
def ok(path):
    if path not in _checked:
        try:
            req = urllib.request.Request(BASE + path, headers={"User-Agent": "barus-backlog"})
            code = urllib.request.urlopen(req, timeout=15).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = type(e).__name__
        time.sleep(0.5)
        _checked[path] = code
        if code != 200:
            print("не открылся:", code, BASE + path)
    return _checked[path] == 200

def link(text, path):
    if path and ok(path):
        return '<a href="%s%s" target="_blank" rel="noopener">%s</a>' % (BASE, path, text)
    return text

items = json.load(open("items.json", encoding="utf-8"))
rows = []
for it in items:
    rows.append("<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class=\"st %s\">%s</td></tr>" % (
        it["id"],
        link(it["category"], it.get("category_url")),
        link(it["subcategory"], it.get("subcategory_url")),
        link(it["series"], it.get("series_url")),
        link(it["product"], it.get("product_url")),
        it["problem"], it["kind"], it["status"]))
html = (HEAD + '<p class="upd">Обновлено %s</p>\n<table>\n' % datetime.date.today().strftime("%d.%m.%Y")
        + COLS + "\n<tbody>\n" + "\n".join(rows) + "\n</tbody></table>\n</div></body></html>\n")
open("index.html", "w", encoding="utf-8").write(html)
print("пунктов:", len(items), "ссылок:", html.count("<a href="), "не открылось:", sum(v != 200 for v in _checked.values()))
