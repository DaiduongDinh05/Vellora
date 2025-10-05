
## Dev guide

### Setup

#### 1. Clone repo
```
git clone https://github.com/Stack-Underflow-Capstone/Velora.git](https://github.com/Stack-Underflow-Capstone/Vellora.git
```

#### 2. Create and activate a virtual environment (Windows idk how on mac)
```
python -m venv .venv
.venv\Scripts\activate
```
You should see (.venv) at the beginning of your terminal line if this worked

#### 3. Install dependencies
```
pip install -r requirements.txt
```

If you install any new package later `pip install somepackage`, always update the requirements file:
```bash
pip freeze > requirements.txt
```

#### 4. Set up your `.env` ONLY for when github actions isnt setup
Create a file named `.env` in the project root (same level as `app/`):

```
DATABASE_URL=bla
```

### Run the app
To run the FastAPI development server:
```
fastapi dev app/main.py
```
Documentation (swagger) : http://127.0.0.1:8000/docs

### Creating a new feature

#### 1. Create folder in module folder

ex:
```
app/modules/trips/
```

#### 2. Inside it, create these files and write your code:

```
router.py        # FastAPI endpoints
service.py       # Business logic
repository.py    # DB queries (using async SQLAlchemy)
models.py        # ORM models (inherit from Base)
schemas.py       # Pydantic request/response models
__init__.py
```

#### 2. Inside it, create these files and write your code:

Alembic only sees your models if they’re imported inside:
```
app/infra/migrations/env.py
```

So add this line at the top:
```python
from app.modules.trips import models  #"app.modules.<name of folder>"
```

That’s all don’t modify anything else in `env.py`.

#### 3. Generating and Applying Migrations

Whenever you add or change a model:

First Generate a migration file
```
alembic revision --autogenerate -m "desc of what u did in model"
```
Then Apply the migration
```
alembic upgrade head
```
You can undo migrations if u ever need to.

#### 4. Registering your router

After creating your router, you must include it in the global API.

Open:
```
app/api/v1/router.py
```
Add:
```python
from app.modules.trips.router import router as trips_router #app.modules.<folder name>.router
router.include_router(trips_router)
```

