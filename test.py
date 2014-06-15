from cluster_commander.commander import Commander
from cluster_commander.cluster.default_layout import DefaultLayout

d = DefaultLayout()
c = Commander(d, {'hostname': 'hostname'})
c.execute_command_on_cluster('hostname')
