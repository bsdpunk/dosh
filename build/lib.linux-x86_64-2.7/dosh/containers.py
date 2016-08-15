from docker import Client

def containers(api):
    cli = Client(base_url='tcp://'+api['docker-ip']+':2375')
    return cli.containers()
