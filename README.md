# CRUD Telegram Bot

![Python](https://img.shields.io/badge/Python-v^3.11-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v^2.0.20-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/hackersandslackers/sqlalchemy-tutorial.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/hackersandslackers/sqlalchemy-tutorial/issues)
[![GitHub Stars](https://img.shields.io/github/stars/hackersandslackers/sqlalchemy-tutorial.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/hackersandslackers/sqlalchemy-tutorial/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/hackersandslackers/sqlalchemy-tutorial.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/hackersandslackers/sqlalchemy-tutorial/network)

This repository contains the source code of a Telegram Bot app which allows to interact with a DB:

## Getting Started

Get set up locally in two steps:

### Environment Variables

Add a env file with your values and rename this file to **.env**:

* `DATABASE_USER`: Username for a SQL database.
* `DATABASE_PASSWORD`: Corresponding password for the above SQL database user.
* `DATABASE_HOST`: Host of the SQL database.
* `DATABASE_PORT`: Numerical port of the SQL database.
* `DATABASE_TABLE`: Name of the SQL database table.

*Remember never to commit secrets saved in .env files to Github.*

### Installation