from op.backend.base import Model


class App(Model): pass


class Build(Model):
    prefix = 'build/{app}'


class Buildpack(Model): pass


class Config(Model):
    prefix = 'instance/{app}/{instance}'


class Instance(Model):
    prefix = 'instance/{app}'


class Node(Model): pass


class Release(Model):
    prefix = 'release/{app}/{instance}'


class Replica(Model):
    prefix = 'replica/{app}/{instance}/{release}'


class Squad(Model): pass
