import json
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
        split_revision = code_revision.split('.')
        id_revision = split_revision[0]
        build_release = split_revision[1]
        build_hotfix = split_revision[2]
        list_artifact = artifacts.split(',')
        try:
            input_request = {'id_ticket': id_ticket, 'id_type_tech': id_type_tech, 'id_revision': id_revision,
                             'build_release': build_release, 'build_hotfix': build_hotfix,
                             'modification_user': modification_user, 'artifacts': list_artifact}
            json_request = json.dumps(input_request)
            # print json_request
            url_request = 'http://%s/process_ticket' % server_port
            result = requests.post(url_request, data=json_request, headers=header)
            if result.status_code == 200:
                json_result = json.loads(result.content)
                # print 'result status_code 200'
                if json_result['result'] == 'OK':
                    print 'ticket process successfully'
                else:
                    print result.content
            else:
                message = 'error_code: %s, content: %s' % (result.status_code, result.content)
                print message
        except RuntimeError as e:
            print e.message
    else:
        sys.stdout.write("error, missing options. It should be id_ticket, code_artifact, id_type_tech")
