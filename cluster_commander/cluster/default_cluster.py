from cluster_commander.cluster.cluster import Cluster


class DefaultCluster(Cluster):
    def __init__(self, name, data_source):
        self._nodes = data_source['nodes']
        self._min_replication = data_source.get('min_replication', 1)
        self.name = name

    def nodes(self):
        return self._nodes

    def is_safe(self, todo, done):
        return len(todo | done) >= self._min_replication

    def __repr__(self):
        return "DefaultCluster({0} :-> {1})".format(self.name, self.nodes())
