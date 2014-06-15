from cluster_commander.cluster.cluster import Cluster


class DefaultCluster(Cluster):
    def __init__(self, name, service_yaml):
        self._nodes = service_yaml['nodes']
        self._shards = service_yaml['shards']
        self._min_replication = service_yaml['min_replication']
        self._node_to_shard = service_yaml['node_to_shard']
        self.name = name

    def nodes(self):
        return self._nodes

    def is_safe(self, todo, done):
        shards = dict((shard, 0) for shard in self._shards)
        for node in todo | done:
            for shard in self._node_to_shard[node]:
                shards[shard] += 1
        return all(repl >= self._min_replication
                   for shard, repl in shards.iteritems())

    def __repr__(self):
        return "DefaultCluster({0} :-> {1})".format(self.name, self.nodes())
