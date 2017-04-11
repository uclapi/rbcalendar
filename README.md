# rbcalendar

## Setup

### Dependencies
- Postgres Server
- Redis Server

### Installation
- Clone this repository
- `cd` into the folder
- run `cp .env.example .env` and fill in the necessary values in .env
- Create a new virtual environment
- Run `pip install -r requirements.txt`

- Make sure both Postgres and Redis are running (you can start redis by running `redis-server`)
- Start the beat scheduler by running `celery -A rbcalendar beat`
- Start the celery worker by running `celery -A rbcalendar worker -l info`
- Start django by running `python manage.py runserver`
- Go to http://localhost:8000
- :tada:
