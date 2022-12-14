# CSFLE Manual Encryption skeleton code

from pymongo import MongoClient
from pymongo.errors import EncryptionError, ServerSelectionTimeoutError, ConnectionFailure
from bson.codec_options import CodecOptions
from pymongo.encryption import Algorithm
from bson.binary import STANDARD
from pymongo.encryption import ClientEncryption
from datetime import datetime
import sys


def mdb_client(db_data):
  try:
    client = MongoClient(db_data['DB_CONNECTION_STRING'], serverSelectionTimeoutMS=db_data['DB_TIMEOUT'], tls=True, tlsCAFile=db_data['DB_SSL_CA'])
    client.admin.command('hello')
    return client, None
  except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    return None, f"Cannot connect to database, please check settings in config file: {e}"

def main():

  # Obviously this should not be hardcoded
  config_data = {
    "DB_CONNECTION_STRING": "mongodb://app_user:<PASSWORD>@csfle-mongodb-<PETNAME>.mdbtraining.net",
    "DB_TIMEOUT": 5000,
    "DB_SSL_CA": "/etc/pki/tls/certs/ca.cert"
  }


  keyvault_namespace = f"__encryption.__keyVault"
  provider = "kmip"

  kms_provider = {
    provider: {
      "endpoint": "csfle-kmip-<PETNAME>.mdbtraining.net"
    }
  }
  
  encrypted_db_name = "companyData"
  encrypted_coll_name = "employee"

  client, err = mdb_client(config_data)
  if err != None:
    print(err)
    sys.exit(1)


  client_encryption = ClientEncryption(
    kms_provider,
    keyvault_namespace,
    client,
    CodecOptions(uuid_representation=STANDARD),
    kms_tls_options = {
      "kmip": {
        "tlsCAFile": "/etc/pki/tls/certs/ca.cert",
        "tlsCertificateKeyFile": "/home/ec2-user/server.pem"
      }
    }
  )

  # retrieve the DEK UUID
  data_key_id_1 = # Put code here to find the _id of the DEK we created previously

  payload = {
    "name": {
      "firstName": "Manish",
      "lastName": "Engineer",
      "otherNames": None,
    },
    "address": {
      "streetAddress": "1 Bson Street",
      "suburbCounty": "Mongoville",
      "stateProvince": "Victoria",
      "zipPostcode": "3999",
      "country": "Oz"
    },
    "dob": datetime(1980, 10, 10),
    "phoneNumber": "1800MONGO",
    "salary": 999999.99,
    "taxIdentifier": "78SD20NN001",
    "role": [
      "CTO"
    ]
  }

  try:

    # put your code here to encrypt the required fields
    # Don't forget to handle to event of name.otherNames being null

  except EncryptionError as e:
    print(f"Encryption error: {e}")


  print(payload)

  result = client[encrypted_db_name][encrypted_coll_name].insert_one(payload)

  print(result.inserted_id)

if __name__ == "__main__":
  main()