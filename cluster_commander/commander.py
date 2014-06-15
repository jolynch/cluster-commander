import time
from fabric.api import task, run, parallel, execute, env, settings


@task
@parallel
def execute_command_parallel(cmd):
    run(cmd)


class Commander(object):
    """Commands nodes to execute the command subject to cluster health
       constraints.

    :param cluster_layout: A python object conforming to the
           :interface:ClusterLayout interface. Provides information about
           cluster that you want managed by this Commander
    :param command_provider: A python dictionary containing mappings from
           human readable commands to full command lines.

           e.g. 'reload' -> 'sudo invoke-serviceinit <service> reload'
    """
    def __init__(self, cluster_layout, command_provider):
        self.cluster = cluster_layout.get_cluster()
        self.command_provider = command_provider

    def execute_command_on_nodes(self, nodes, command, callback):
        """Executes a command on a list of nodes

        :param nodes: A list of hostnames to execute the command on
        :param command: A shorthand command that will be looked up in the
                        command provider
        :param callback: A callback to call when done with the command
        """
        cmd = self.command_provider[command]
        print "Executing {0} on {1}".format(cmd, nodes)
        with settings(skip_bad_hosts=True, warn_only=True,
                      connection_attempts=3, timeout=2):
            result = execute(execute_command_parallel,
                             hosts=list(nodes), cmd=cmd)
        for node, node_result in result.iteritems():
            callback(node, node_result)

    def execute_command_on_cluster(self, command):
        """Single pass driver that tries to execute a command on a cluster
           while ensuring safety

           This uses a greedy algorithm to try to move as many hosts
           as possible to the "doing" set while preserving cluster
           constraints which are checked by calling self.cluster.is_safe
        """
        if not self.cluster.nodes():
            return 0

        todo   = set(self.cluster.nodes())
        doing  = set()
        done   = set()
        failed = set()

        def move_to_doing(node):
            todo.remove(node)
            doing.add(node)

        def move_from_doing(node, exit):
            doing.remove(node)
            if exit is None:
                done.add(node)
            else:
                failed.add((node, exit))

        while todo:
            # Find a candidate set
            candidate_set = set()
            for candidate in todo:
                potential_candidate_set = candidate_set | set([candidate])
                if self.cluster.is_safe(todo - potential_candidate_set, done):
                    candidate_set = potential_candidate_set

            # If no forward progress can be made without violating the cluster
            # constraints, fail now
            if len(candidate_set) == 0 and len(doing) == 0:
                print "Refusing to proceed in command issuing. No safe choice"
                break

            # Execute the command on the candidates in parallel
            for candidate in candidate_set:
                move_to_doing(candidate)
            self.execute_command_on_nodes(candidate_set,
                                          command, move_from_doing)

        self.report_result(self.cluster, command, todo, done, failed)

    def report_result(self, cluster, command, todo, done, failed):
        print "Applied {0} to {1}".format(command, cluster)
        print "Done: {0}".format(done)
        print "Failed {0}".format(failed)
