# Бэклог проблем в данных заказчика

Страница: https://rodrigesdmitriy-ux.github.io/barus-backlog/

Пункты живут в `items.json`, `index.html` собирается скриптом, руками его не правим.

## Как добавить пункт

1. Добавить объект в конец `items.json` со следующим `id`.
2. `python3 render.py` (проверит ссылки на сайте, недоступные напечатает и оставит текстом).
3. `git commit -am "Бэклог: пункт N"` и `git push`.

## Поля

`id`, `category`, `subcategory`, `series`, `product` (можно `<br>`), `problem` (HTML, только `ul`, `li`, `br`), `status`, `kind` (`open` или `done`), `category_url`, `subcategory_url`, `series_url`, `product_url` (необязательно). Адреса относительные, от корня сайта; адреса разделов берём из `structure-v6/barus-struktura.csv`.

## Правила

- Пункты не удаляем. У решённого меняем `status` и ставим `kind: "done"`.
- Текст читает заказчик: без длинных тире и служебных фраз.
- Цены фабрики в бэклог не пишем.
