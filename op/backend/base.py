import os
from etcd import EtcdKeyNotFound


class Model(object):
    prefix = None

    def __init__(self, etcd=None, key=None, result=None, **kwargs):
        self.etcd = etcd

        if result is not None:
            self.result = result

        elif key is not None:
            self.result = self.get(etcd, key, **kwargs)

    def after_create(self): pass

    @classmethod
    def build_key(cls, key, **kwargs):
        prefix = cls.__name__.lower()

        if cls.prefix is not None:
            prefix = cls.prefix.format(**kwargs.get('key_args', {}))

        return os.path.join(os.getenv('ETCD_PREFIX', 'op'), os.path.join(prefix, key))

    @classmethod
    def create(cls, etcd, key, value=None, **kwargs):

        main_key = cls.build_key(key, **kwargs)
        key_args = kwargs.pop('key_args') if 'key_args' in kwargs else {}

        if kwargs.keys():
            object_prefix = key

            if value is not None:
                object_prefix = os.path.join(key, value)

            for k, value in kwargs.items():
                cls.get_or_create(
                    etcd,
                    os.path.join(object_prefix, k),
                    value=value,
                    **dict(key_args=key_args)
                )

            obj = cls.instantiate(key, etcd.read(main_key))

        else:
            obj = cls.instantiate(key, etcd.write(main_key, value))

        if isinstance(obj, Model):
            obj.after_create()

        return obj

    @classmethod
    def instantiate(cls, key, result):
        return cls(result) if '/' not in key else result

    @classmethod
    def get(cls, etcd, key, **kwargs):
        try:
            return cls.instantiate(key, etcd.read(cls.build_key(key, **kwargs)))
        except EtcdKeyNotFound:
            return None

    @classmethod
    def get_or_create(cls, etcd, key, value=None, **kwargs):
        existing = cls.get(etcd, key, **kwargs)
        if existing is not None:
            return existing

        return cls.create(etcd, key, value, **kwargs)
