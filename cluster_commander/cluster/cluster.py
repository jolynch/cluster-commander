

class Cluster(object):
    def nodes(self):
        raise NotImplementedError()

    def is_safe(self, todo, done):
        raise NotImplementedError()
