![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Build CI](https://github.com/nico-fst/dabstar-wedding.de/actions/workflows/build.yml/badge.svg)

# Dabstar-Wedding.de

A wedding page focused on a clean and simple, yet beige-stunning look.

- saves validated RSVPs in `db.sqlite3` in `wedsite_data/` as volume
- .env should provide:

```yml
SECRET_KEY=<...>
DEBUG=<True|False>
ALLOWED_HOSTS=<dabstar-wedding.de, ...>
DROPZONE_URL=<https://...>
```

# Deploy

- via `docker-compose up --build -d`
  - without cache (e.g. when changing env):
    - `docker-compose build --no-cache`
    - `docker-compose up -d`

---

# Credits

- ([HTML/CSS/JS Code I used and adapted for this website](https://themewagon.com/themes/free-bootstrap-wedding-website-template/)) not used anymore
- [Favicon](https://icon-icons.com/download/144595/ICO/512/)