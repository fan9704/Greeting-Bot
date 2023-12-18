# Greeting Bot Learn Note

---

## Django MongoDB ODM(Djongo) Note

WARNING **Djongo 1.3.6 not support Django 4.2**

### Step.1 Install Dependencies

```shell
pipenv install dnspython pymongo djongo pytz sqlparse
```

### Step.2 Setup Mongo Environment

In .env
```shell
MONGO_DB=
MONGO_TEST_DB=
MONGO_ROOT_USER=
MONGO_ROOT_PASSWORD=
MONGO_USER=
MONGO_PASSWORD=
MONGO_DB_URL=
MONGO_DB_PORT=
```

### Step.3 Configure Django Project Database

In settings.py
```python
import os 
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'greet',
        'CLIENT': {
            'host': f'mongodb://{os.getenv("MONGO_DB_URL", "127.0.0.1")}:{os.getenv("MONGO_DB_PORT", 27017)}',
            'port': int(os.getenv("MONGO_DB_PORT", 27017)),
        }
    },
}
```

Then Complete

Notice Djongo not support deepsearch like filter birthday by day and month