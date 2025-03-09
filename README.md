![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Build CI](https://github.com/nico-fst/dabstar-wedding.de/actions/workflows/build.yml/badge.svg)

# Dabstar-Wedding.de

A wedding page focused on a clean and simple, yet stunning beige look.

![dabstar-wedding mobile 4th WIDE TITLED BOLD](https://github.com/user-attachments/assets/ba546321-313b-4191-9c4a-e856c2fdfd24)

Built to run as Docker Container - saves validated RSVPs in `db.sqlite3` in `wedsite_data/` as volume

# Deploy

- .env should provide:

```yml
SECRET_KEY=<...>
DEBUG=<True|False>
ALLOWED_HOSTS=<dabstar-wedding.de, ...>
DROPZONE_URL=<https://...>
PW_ANTWORTEN=<...>
```

- via `docker-compose up --build -d`
  - without cache (e.g. when changing env):
    - `docker-compose build --no-cache`
    - `docker-compose up -d`

# Multi-Language support

`I18N` and `L10N` configured in settings.py using middleware, urlpatterns adapted. To translate text, follow these theps:

1. Replace e.g. `<p>Hallo Hochzeitsseite</p>` with `<p>{% trans "Hallo Hochzeitsseite %}</p>`
2. Create Translation .po files with
  - `python3 manage.py makemessages -l en`
  - `python3 manage.py makemessages -l de`
3. Add translations in the .po files, e.g.:

```
msgid "Hallo Hochzeitsseite"
msgstr "Hello Wedsite"
```

4. Coompile .po files to .mo files via `python3 manage.py compilemessages`

---

# Credits

- [Favicon](https://icon-icons.com/download/144595/ICO/512/)
