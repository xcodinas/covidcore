# Deletos API

## Database requirements:
You will need to install postgis and enable it on the api database.
To do that first you need to install the package:

```sh
$ sudo apt-get install postgis
```

## Install requirements:
 ```sh
$ sudo apt-get install postgi
$ python setup.py develop
```

## Instalation
 ```sh
$ flask db init
$ flask db migrate
$ flask db upgrade
```

### Documentation
In order to make the documentation work you will need to follow these steps:

 ```sh
$ cd app/static
$ npm install
```

## Testing
 ```sh
$ python setup.py test
```

## Error Codes Notation
0xx -> Beta
1xx -> User
2xx -> Deleto
3xx -> Notification
4xx -> Message
5xx -> Crush
6xx -> Follow
7xx -> Demojis
:D
