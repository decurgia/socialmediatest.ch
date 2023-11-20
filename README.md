# socialmediacert

Social Media Certification

## Documentation

https://github.com/gldecurtins/socialmediacert/wiki

## Docker development setup

```
cd ~
git clone https://github.com/gldecurtins/socialmediacert
docker-compose up
```

## Python Virtual Environment development setup

```
cd ~
git clone https://github.com/gldecurtins/socialmediacert
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
python3 manage.py check
```

## Configuration

Export some environment variables.

### SECRET_KEY

Set your own value, e.g. a 50 character random string.
https://docs.djangoproject.com/en/3.2/topics/signing/

```
SECRET_KEY = ''
```
