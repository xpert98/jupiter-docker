import docker
import rsa
import base64
import jwt
import random
import string
import uuid
import argparse

def create_aes_key():
    (pubkey, privkey) = rsa.newkeys(512)
    aes_key = rsa.randnum.read_random_bits(128)
    encrypted_aes_key = rsa.encrypt(aes_key, privkey)
    encoded_key = base64.b64encode(encrypted_aes_key)
    return encoded_key

def create_jwt(encoded_aes_key):
    encoded_jwt = jwt.encode({'collector': '0'}, encoded_aes_key, algorithm='HS256')
    return encoded_jwt

def create_random_string(pw_len):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = pw_len))
    return random_string 

parser = argparse.ArgumentParser()

parser.add_argument('-v', action='store', dest='secret_ver', required=True)

cmdln_args = parser.parse_args()

client = docker.from_env()

#imc
imcdb_password = create_random_string(12)
client.secrets.create(
    name='imcdb_password'+str(cmdln_args.secret_ver),
    data=imcdb_password
) 

print("imcdb password v"+str(cmdln_args.secret_ver)+": ", imcdb_password)

imc_secret_key = create_aes_key()
client.secrets.create(
    name='imc_secret_key'+str(cmdln_args.secret_ver),
    data=imc_secret_key.decode()
) 

print("imc secret key v"+str(cmdln_args.secret_ver)+": ", imc_secret_key.decode())

imc_secret_iv = create_random_string(48)
client.secrets.create(
    name='imc_secret_iv'+str(cmdln_args.secret_ver),
    data=imc_secret_iv
) 

print("imc secret iv v"+str(cmdln_args.secret_ver)+": ", imc_secret_iv)

print("\n")

#cis
cisdb_password = create_random_string(12)
client.secrets.create(
    name='cisdb_password'+str(cmdln_args.secret_ver),
    data=cisdb_password
) 

print("cisdb password v"+str(cmdln_args.secret_ver)+": ", cisdb_password)

cis_jwt_secret = create_aes_key() 

cis_jwt = create_jwt(cis_jwt_secret.decode()) 

client.secrets.create(
    name='cis_jwt_secret'+str(cmdln_args.secret_ver),
    data=cis_jwt_secret.decode()
) 

print("cis secret v"+str(cmdln_args.secret_ver)+": ", cis_jwt_secret.decode())

print("cis jwt v"+str(cmdln_args.secret_ver)+": ", cis_jwt.decode())

print("\n")

#cs
mongo_root_password = create_random_string(12)
client.secrets.create(
    name='mongo_root_password'+str(cmdln_args.secret_ver),
    data=mongo_root_password
) 

print("mongo root password v"+str(cmdln_args.secret_ver)+": ", mongo_root_password)

mongo_user_password = create_random_string(12)
client.secrets.create(
    name='mongo_user_password'+str(cmdln_args.secret_ver),
    data=mongo_user_password
) 

print("mongo user password v"+str(cmdln_args.secret_ver)+": ", mongo_user_password)

cs_jwt_secret = create_aes_key() 

cs_jwt = create_jwt(cs_jwt_secret.decode()) 

client.secrets.create(
    name='cs_jwt_secret'+str(cmdln_args.secret_ver),
    data=cs_jwt_secret.decode()
) 

print("cs secret v"+str(cmdln_args.secret_ver)+": ", cs_jwt_secret.decode())

print("cs jwt v"+str(cmdln_args.secret_ver)+ ": ", cs_jwt.decode())

cs_instance_id = uuid.uuid4()
client.secrets.create(
    name='cs_instance_id'+str(cmdln_args.secret_ver),
    data=str(cs_instance_id)
)

print("cs instance id v"+str(cmdln_args.secret_ver)+": ", cs_instance_id)
#client = docker.from_env()

print("\n")

mongo_init_file = open("init-mongo.js", "w")
mongo_init_file.write('db.createUser({user: "jupiter",pwd: "'+mongo_user_password+'",roles: [ "readWrite"]});')
mongo_init_file.write('db.createCollection("inventories");')
mongo_init_file.close()

docker_compose_template = open("docker-compose.yaml.template", "r")
docker_compose_out = open("docker-compose.yaml", "w")
for line in docker_compose_template:
    docker_compose_out.write(line.replace('#', str(cmdln_args.secret_ver)))
docker_compose_template.close()
docker_compose_out.close()
