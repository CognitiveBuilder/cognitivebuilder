from io import StringIO
import json
import requests
                                    
# This functfion accesses a file in your Object Storage. The definition contains your credentials.
# You might want to remove those credentials before you share your notebook.
def notebook_xfer(container, filename, write_data=None):
    """This functions returns a StringIO object containing
    the file content from Bluemix Object Storage."""

    url1 = ''.join(['https://identity.open.softlayer.com', '/v3/auth/tokens'])
    data = {'auth': {'identity': {'methods': ['password'],
            'password': {'user': {'name': 'YOUR_BLUEMIX_MEMBER_CREDENTIAL','domain': {'id': 'YOUR_BLUEMIX_CREDENTIAL'},
            'password': 'YOUR_BLUEMIX_PASSWORD_CREDENTIAL'}}}}}
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    resp1_body = resp1.json()
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                        if(e2['interface']=='public'and e2['region']=='dallas'):
                            url2 = ''.join([e2['url'],'/', container, '/', filename])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
    if write_data:
        resp2 = requests.put(url=url2, headers=headers2, data=write_data)
    else:
        resp2 = requests.get(url=url2, headers=headers2)
    if resp2.status_code//100 != 2:
        raise Exception( resp2.status_code,  resp2.text )
    return StringIO(resp2.text)

def get_to_file(notebook,remote_file,local_file):
    text = notebook_xfer(notebook,remote_file)
    with open(local_file,"w") as f:            
        f.write(text.read())
        
def put_from_file(notebook,remote_file,local_file):
    with open(local_file,"r") as f:
        notebook_xfer(notebook,remote_file,f.read())
