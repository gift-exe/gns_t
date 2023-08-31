from gns3fy import Gns3Connector, Project
from build_topo import TopoBuilder


server = Gns3Connector('http://localhost:3080')
project = Project(name='test2', connector=server)
project.get()

topo = TopoBuilder(server=server, project=project)
topo.build(9, 3, 3)