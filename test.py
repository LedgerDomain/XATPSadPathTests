import requests
import json
import time
import sys
import getopt

def main(argv):

    API_KEY = ''
    VERIFY_URL = ''
    opts, args = getopt.getopt(argv,"hk:u:",["key=","url="])
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -k <api_key> -u <verify_endpoint_url>')
        if opt in ('-k', '--key'):
            API_KEY = arg
        if opt in ('-u', '--url'):
            VERIFY_URL = arg
    if API_KEY == '' or VERIFY_URL == '':
        print('Please supply both an API Key and the URL of the API endpoint for credential verification')
    else:    
        run_tests(API_KEY, VERIFY_URL)
    
def run_tests(api_key, verify_url):
    with open('sad-path-tests.json', 'r') as f:
        test_cases = json.loads(f.read())
        
    win_count = 0

    for i in range(len(test_cases)):
        r = requests.post(verify_url,
                          headers = {
                              'Content-Type': 'application/json',
                              'X-API-KEY' : api_key,
                          },
                          json=test_cases[i]['params'])
        response = r.json()
        response_str = json.dumps(response)
        expected_response_str = json.dumps(test_cases[i]['response'])
        if response_str != expected_response_str:
            print('Case {} failed\n\nExpected:\n\n{}\n\nBut got:\n\n{}\n_______'.format(i, expected_response_str, response_str))
        else:
            win_count += 1
        time.sleep(.1)
    print('{}/{} tests completed successfully'.format(win_count, len(test_cases)))
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
