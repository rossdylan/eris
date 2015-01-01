I stumbled upon the fine bit of python that is
[kragniz/json-sempai](https://github.com/kragniz/json-sempai) and was struck
with inspration. So I built a library that lets you import python packages
from a redis server.

# Example Use

## Upload a python file to redis

```
$ cat some_module.py | redis-cli -x set some_module
```

## Import it using Eris

```python
import eris
import some_module
```

# It supports packages as well

## Create a module in redis
```
$ cat some_module/__init__.py | redis-cli -x set some_module.__init__
$ cat some_module/foo.py | redis-cli -x set some_module.foo
```


```python
import eris
from some_module import foo
```


# Notes
You probably shouldn't use this.
