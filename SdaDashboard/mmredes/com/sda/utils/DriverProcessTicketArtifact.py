import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) == 7:
        server_port = sys.argv[1]
        id_ticket = sys.argv[2]
        id_type_tech = sys.argv[3]
        code_revision = sys.argv[4]
        modification_user = sys.argv[5]
        artifacts = sys.argv[6]

        header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        json_request = {'id_ticket': id_ticket, }
        result = requests.post(server_port, data=json_request, headers=header)
    else:
        sys.stdout.write("error, missing options. It should be id_ticket, code_artifact, id_type_tech")
