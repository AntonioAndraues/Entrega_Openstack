import os
import openstack
def create_connection(auth_url, region, project_name, username, password):

    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
	domain_name="domain_admin",
        app_name='examples',
        app_version='1.0',
    )

def list_users(conn):
    print("List Users:")

    for user in conn.identity.users():
        print(user)
def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)
def list_flavors(conn):
    print("List Flavors:")

    for flavor in conn.compute.flavors():
        print(flavor)
def create_keypair(conn):
    keypair = conn.compute.find_keypair('id_rsa')

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name='id_rsa')

        print(keypair)

        try:
            os.mkdir('../.ssh2/')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open('id_rsa', 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod('id_rsa', 0o400)

    return keypair

con=create_connection(auth_url="http://192.168.0.18:5000/v3",project_name="admin",username="admin",password="uShaeThae7Ga7yah",region="RegionOne")
#list_users(con)
list_servers(con)
#list_flavors(con)
#print(con.compute.flavors())
#print(con)
#print(con.compute)
#print(con.compute.find_flavor('m1.small'))
def create_server(conn):
    print("Create Server:")

    image = conn.compute.find_image('bionic')
    flavor = conn.compute.find_flavor('m1.small')
    network = conn.network.find_network('antonioandraues_network')
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name='teste12211221', image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = conn.compute.wait_for_server(server)

    print("ssh -i {key} root@{ip}".format(
        key='id_rsa',
        ip=server.access_ipv4))
create_server(con)
print("Delete Server:")
server = con.compute.find_server('teste12211221')
print(server)
con.compute.delete_server(server)
