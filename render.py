#!/usr/bin/env python3
"""Собирает index.html из items.json. Запуск: python3 render.py"""
import html, json, time, datetime, zoneinfo, urllib.request, urllib.error

BASE = "https://barus.skalkindmitriy.ru"
HEAD = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Каталог: вопросы по данным и наши решения</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Russo+One&family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
<style>
body{margin:0;background:#f4f6f8;font:15px/1.6 Montserrat,Tahoma,sans-serif;color:#232323}
.wrap{max-width:1240px;box-sizing:border-box;margin:0 auto;padding:32px 40px 64px;background:#fff}
h1{font-family:'Russo One',Montserrat,sans-serif;font-weight:400;font-size:28px;border-bottom:3px solid #42c1c7;padding-bottom:12px;margin:0 0 8px}
.lead{margin:0 0 4px}.upd{color:#5b6570;font-size:13px;margin:0 0 20px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:#232323;color:#fff;text-align:left;padding:9px 10px;font-weight:600}
th:nth-child(1){width:4%}th:nth-child(2){width:16%}th:nth-child(3){width:28%}th:nth-child(4){width:22%}th:nth-child(5){width:18%}th:nth-child(6){width:12%}
h2{font-family:'Russo One',Montserrat,sans-serif;font-weight:400;font-size:21px;margin:36px 0 4px}.sec{margin:0 0 10px;font-size:14px}
.toc{margin:0 0 20px;padding-left:20px}.toc span{color:#5b6570;font-size:13px}
td{overflow-wrap:anywhere}
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
td:nth-child(2)::before{content:"Где"}
td:nth-child(3)::before{content:"Проблема"}
td:nth-child(4)::before{content:"Наше решение"}
td:nth-child(5)::before{content:"Что нужно от вас"}
td:nth-child(6)::before{content:"Статус"}
td:empty{display:none}
}
@media print{body{background:#fff}.wrap{padding:0}tr{break-inside:avoid}}
</style></head><body><div class="wrap">
<h1>Каталог: вопросы по данным и наши решения</h1>
<p class="lead">Замечания сгруппированы по разделам каталога, в каждой строке проблема, что мы уже сделали на сайте и что нужно от вас.</p>
'''
COLS = "<thead><tr><th>№</th><th>Где</th><th>Проблема</th><th>Наше решение</th><th>Что нужно от вас</th><th>Статус</th></tr></thead>"

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
        time.sleep(3)  # сайт отвечает 503 на частые запросы
        _checked[path] = code
        if code != 200:
            print("не открылся:", code, BASE + path)
    return _checked[path] == 200

def link(text, path):
    if path and ok(path):
        return '<a href="%s%s" target="_blank" rel="noopener">%s</a>' % (BASE, path, text)
    return text

# Порядок разделов как в каталоге на сайте (/catalog/, затем /catalog/machines/)
ORDER = ["Расходные материалы для лазерной резки", "Станки лазерной резки листа", "Станки лазерной резки труб",
         "Листогибочные прессы", "Шлифовально-зачистные станки", "Координатно-пробивные прессы", "Аппараты лазерной сварки",
         "Аппараты импульсной лазерной чистки", "Аппараты постоянной лазерной чистки", "Плазменная расходка"]
COMMON = "Общее для нескольких разделов"
COMMON_CATS = {"Весь каталог", "Лазерная и плазменная расходка"}

items = json.load(open("items.json", encoding="utf-8"))
groups = {k: [] for k in [COMMON] + ORDER}
for it in items:
    c = it["category"]
    groups[COMMON if ";" in c or c in COMMON_CATS else c].append(it)  # KeyError, если появится новый раздел: добавить в ORDER

def where(it, common):
    parts = [link(it[k], it.get(k + "_url")) for k in ("subcategory", "series", "product") if it.get(k)]
    if common:
        parts.insert(0, ", ".join(x.strip() for x in it["category"].split(";")))
    return "<br>".join(parts)

toc, body = [], []
for n, (name, its) in enumerate((k, v) for k, v in groups.items() if v):
    its.sort(key=lambda i: (i["kind"] == "done", i["id"]))
    nd = sum(i["kind"] == "done" for i in its)
    toc.append('<li><a href="#s%d">%s</a> <span>открыто %d, решено %d</span></li>' % (n, name, len(its) - nd, nd))
    url = next((i["category_url"] for i in its if i.get("category_url")), None)
    rows = ['<tr id="p%d"><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class="st %s">%s</td></tr>' % (
        i["id"], i["id"], where(i, name == COMMON), i["problem"], i.get("solution") or "",
        html.escape(i.get("ask", ""), quote=False), i["kind"], i["status"]) for i in its]
    sec = '<p class="sec"><a href="%s%s" target="_blank" rel="noopener">Раздел на сайте</a></p>\n' % (BASE, url) if url and ok(url) else ""
    body.append('<h2 id="s%d">%s</h2>\n%s<table>\n%s\n<tbody>\n%s\n</tbody></table>' % (n, name, sec, COLS, "\n".join(rows)))

today = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Moscow")).strftime("%d.%m.%Y")
page = (HEAD + '<p class="upd">Обновлено %s</p>\n<ul class="toc">\n%s\n</ul>\n' % (today, "\n".join(toc))
        + "\n".join(body) + "\n</div></body></html>\n")
open("index.html", "w", encoding="utf-8").write(page)
print("пунктов:", len(items), "ссылок:", page.count("<a href="), "не открылось:", sum(v != 200 for v in _checked.values()))
