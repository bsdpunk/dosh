from docker import Client

def containers(api):
    cli = Client(base_url='tcp://10.1.10.47:2375')
    return cli.containers()
