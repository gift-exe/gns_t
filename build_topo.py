from gns3fy import Node, Link



class TopoBuilder():
    '''
        this class builds a tree topology
        ie. the hybrid topology which is 
        a combination of the star and the bus topology
    '''
    def __init__(self, server, project):
        self.server = server
        self.project = project

    def build(self, n_vpcs, n_switches, n_host_to_switch):
        '''
            call this to build the topology.
            consisting of switches and vpcs (for now)
        '''

        #create vpcs(es)
        for i in range(n_vpcs):
            Node(project_id=self.project.project_id, name=f'pc{i+1}', connector=self.server, template='VPCS').create()

        #create switches
        for i in range(n_switches):
            Node(project_id=self.project.project_id, name=f's{i+1}', connector=self.server, template='Ethernet switch').create()

        #refresh project to get new nodes
        self.project.get()

        #link their asses together

        vpcs = self.project.nodes[:n_vpcs]
        switches = self.project.nodes[n_vpcs:]

        #linking hosts to switches
        for i in range(n_vpcs):
            port = port = (i % n_host_to_switch) + 1
            nodes = [
             dict(node_id=switches[i//3].node_id, adapter_number=0, port_number=port),
             dict(node_id=vpcs[i].node_id, adapter_number=0, port_number=0)
            ]

            Link(project_id=self.project.project_id, nodes=nodes, connector=self.server).create()
        

        #connecte switches to eachother like so : 1 <---> 1 <---> 1 : this is the "bus" part of the topology
        for i in range(n_switches-1):
            port = (i % 2) + (n_host_to_switch + 1)
            nodes = [
                dict(node_id=switches[i].node_id, adapter_number=0, port_number=port),
                dict(node_id=switches[i+1].node_id, adapter_number=0, port_number=port),        
            ]
            Link(project_id=self.project.project_id, nodes=nodes, connector=self.server).create()

        






