from gns3fy import Node, Link
import multiprocessing
from ip_crud import set_ip, get_ip


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
        """
        The `build` function creates a network topology consisting of VPCs and switches, and links them
        together according to a specific pattern.
        
        :param n_vpcs: The parameter `n_vpcs` represents the number of VPCs (Virtual Private Computer Simulators) to be
        created in the topology
        :param n_switches: The parameter `n_switches` represents the number of switches to be created in the
        topology
        :param n_host_to_switch: The parameter `n_host_to_switch` represents the number of hosts that are
        connected to each switch
        :return: a tuple containing two lists: `vpcs` and `switches`.

        :HINT: You should probably call the assign_ips function to give each vpcs their ip addresses
        """

        #create vpcs(es)
        for i in range(n_vpcs):
            node = Node(project_id=self.project.project_id, name=f'pc{i+1}', connector=self.server, template='VPCS')
            node.create()
            node.start()

        #create switches
        for i in range(n_switches):
            node = Node(project_id=self.project.project_id, name=f's{i+1}', connector=self.server, template='Ethernet switch')
            node.create()
            node.start()

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

        return (vpcs, switches)

    def assign_ips(self, vpcs):
        """
        The function assigns IP addresses to VPCs and returns a list of tuples containing the VPC names
        and their corresponding IP addresses.
        
        :param vpcs: The `vpcs` parameter is a list of VPC objects. Each VPC object represents a virtual
        private cloud and has a `name` attribute
        :return: a list of tuples, where each tuple contains the name of a VPC node and its
        corresponding IP address.
        """
        processes = []

        #assign ip addresses to vpcs
        for pc in vpcs:
            addr = f'192.168.1.{pc.name[-1]}'
            gtway = '255.0.0.0'
            process = multiprocessing.Process(target=set_ip, args=[pc, addr, gtway])
            processes.append(process)
            process.start()

        #wait till all the processes run completely before going on
        for process in processes:
            process.join()

        self.project.get()
        vpcs_ips = [(node.name, get_ip(node)) for node in self.project.nodes if node.node_type == 'vpcs']
        return vpcs_ips
            




