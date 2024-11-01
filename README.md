# Postgres vs MySQL

Talbe data resource (Kaggle): https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset/code

## Incept virtual environment

If you use `venv`:

- bash: `source .venv/bin/activate`
- PowerShell `.venv\Scripts\Activate`

## Project Structure

```bash
project-root/
├── docker-compose.yml        # Defines and orchestrates MySQL, PostgreSQL, and other services
├── Dockerfile                # For your Go backend (or separate Dockerfiles if needed)
├── init/
│   ├── start_services.sh     # Script to run Docker Compose and wait for databases to be ready
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py               # Base database class
│   │   ├── postgres.py           # PostgreSQL-specific schema and connection class
│   │   ├── mysql.py              # MySQL-specific schema and connection class (future support)
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_resolver.py      # Class to handle CSV loading and data preparation
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── main.py               # Main script to run the pipeline
└── hotel_reservations.csv        # Sample CSV file
└── README.md
```

## Docker Compose Setting

```yml
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_PASSWORD: example 
    ports:
      - "3000:5432"
    # restart: always
    # set shared memory limit when using docker-compose
    shm_size: 128mb
    # or set shared memory limit when deploy via swarm stack
    #volumes:
    #  - type: tmpfs
    #    target: /dev/shm
    #    tmpfs:
    #      size: 134217728 # 128*2^20 bytes = 128Mb
    networks:
      - my_network
  mysql:
    image: mysql
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: example
    # restart: always
    # set shared memory limit when using docker-compose
    shm_size: 128mb
    # or set shared memory limit when deploy via swarm stack
    #volumes:
    #  - type: tmpfs
    #    target: /dev/shm
    #    tmpfs:
    #      size: 134217728 # 128*2^20 bytes = 128Mb
    networks:
      - my_network

  python_app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - postgres
      - mysql
    environment:
      - PG_HOST=postgres
      - PG_PORT=5432
      - PG_NAME=postgres
      - PG_USER=postgres
      - PG_PASSWORD=example
      - MYSQL_HOST=mysql
      - MYSQL_PORT=3306
      - MYSQL_NAME=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=example
      - MYSQL_DATABASE=mysql
    volumes:
      - .:/app
    networks:
      - my_network

networks:
  my_network:
    driver: bridge
```
