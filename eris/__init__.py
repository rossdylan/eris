import imp
import os
import sys
import redis


class HailErisLoader(object):
    """
    This perversion of the natural order is a custom import loader.  It will go
    out and try to load a python module/package from a redis server. You
    Probably shouldn't be using this.
    """
    def __init__(self):
        """
        We choose what redis server to connect to by the REDIS_SEMPAI_HOST and
        the REDIS_SEMPAI_PORT environment variables.
        """
        self.conn = redis.StrictRedis(
            host=os.getenv('REDIS_SEMPAI_HOST', 'localhost'),
            port=int(os.getenv('REDIS_SEMPAI_PORT', 6379)))

    def find_module(self, name, path=None):
        """
        Go and see if we have the module in redis.
        """
        if self.conn.exists(name):
            return self
        elif self.conn.exists('{0}.__init__'.format(name)):
            return self

    def load_module(self, name):
        """
        logic to actually load the module from redis. Compiled code is grabbed
        using the get_code method. It is then exec'd and turned into a module.
        Eris help you if you decide to actually use this.
        """
        if name in sys.modules:
            return sys.modules[name]
        mod = imp.new_module(name)
        mod.__file__ = 'redis://{0}'.format(name)
        mod.__loader__ = self
        if self.is_package(name):
            mod.__path__ = []
            mod.__package__ = name
        else:
            if len(name.split('.')) > 1:
                mod.__package__ = name.split('.')[0]

        exec(self.get_code(name), mod.__dict__)
        return mod

    def is_package(self, full_name):
        """
        Figured this was the easiest way to check if something is a package.
        (check if a __init__ file is there)
        """
        return self.conn.exists("{0}.__init__".format(full_name))

    def get_code(self, full_name):
        """
        Use the get_source method to grab the source code from redis and
        compile and return it.
        """
        return compile(self.get_source(full_name),
                       'redis://{0}'.format(full_name),
                       'exec')

    def get_source(self, full_name):
        """
        Use the redis get function to actually retrieve the source code for a
        module.
        """
        if self.is_package(full_name):
            return self.conn.get('{0}.__init__'.format(full_name))
        else:
            return self.conn.get(full_name)

sys.meta_path.append(HailErisLoader())
