# Social Media Test

Social Media Test & Certificate

## Documentation

https://github.com/gldecurtins/socialmediatest/wiki

## Docker development setup

```
cd ~
git clone https://github.com/gldecurtins/socialmediatest
docker-compose up
```

## Translations

```
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l de
pybabel update -i messages.pot -d translations
pybabel compile -d translations
```
