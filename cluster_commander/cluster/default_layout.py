from cluster_commander.cluster.layout import Layout
from cluster_commander.cluster.default_cluster import DefaultCluster
import pkgutil
import yaml


class DefaultLayout(Layout):
    @staticmethod
    def get_cluster():
        test_service = pkgutil.get_data('cluster_commander',
                                        'config/services/test_service.yaml')
        test_cluster = DefaultCluster('test_service', yaml.load(test_service))
        return test_cluster

