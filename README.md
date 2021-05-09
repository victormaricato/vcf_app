# Overview

This project serves the purpose of creating a SQL database to store a VCF-like file containing variants data.
Then, the database is accessed through an interface which has a single input bar that must handle either `RSID` and `CHROMOSOME POSITION` queries.

This is all done in less than ~500ms for 95% of the queries using PostgreSQL and FASTAPI.

# Running

You will require [Docker](https://docs.docker.com/engine/) and [docker-compose](https://docs.docker.com/compose/) to run the app.

Also, you will need Python and Make installed in your machine due to the "database population" script.

```
1. Put the desired `{}.vcf.gz` inside `database/data`
2. pip install -r database/requirements.txt
3. make run
```

`make run` will start the database, frontend and backend containers, and then it will populate the database.

Access the frontend at: http://127.0.0.1:4243 and the swagger UI at: http://127.0.0.1:4242/docs.

If you used the default `.vcf.gz` provided, you can test the frontend with: `1 10177` or `rs540431307` (different variant)

![Peek 2021-05-08 23-33](https://user-images.githubusercontent.com/11489228/117558686-d52ae900-b055-11eb-900d-37d7401bbcfb.gif)


# Coding Decisions

## Database

At first, the database of choice was [tiledb-vcf](https://github.com/TileDB-Inc/TileDB-VCF). However, after facing several incompatibilities between the VCF and TileDB, PostgreSQL partitioned by chromosome seemed scalable and easy to deploy.

## API

FastAPI was chosen due to its increased speed when compared with Flask and web2py frameworks. As a plus, FastAPI allows for easy in-code documentation with pydantic models and schemas. Moreover, FastAPI offers several layers of compatibility with PostgreSQL through SQLAlchemy and Pydantic.

