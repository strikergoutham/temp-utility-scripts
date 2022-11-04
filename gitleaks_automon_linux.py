import subprocess
import os
import json
import requests
#import slack
from dotenv import load_dotenv
import glob
from datetime import date

load_dotenv()
API_KEY = os.getenv("GIT_TOKEN")
slack_token = os.getenv("SLACK_TOKEN")
repo_url_str = "https://github.com/<yourORGNAMEHERE>/"

slack_channel = "#test"
#client = slack.WebClient(token=slack_token)
today = date.today()
Msg1 = "*[+]Gitleaks Auto Monitoring Scan Started. Scan Date :* " + str(today) + "\n"
#response = client.chat_postMessage(channel=slack_channel, text=Msg1)

leak_repo = []
print("[+]cleaning up...")
os.system("rm -f *.json")

repos = open("monitored_repos.txt")
for repo in repos:
    repo_name = repo.rstrip()
    print("[+]Scanning Repository: ",repo_name)
    repo_url = repo_url_str + repo_name
    results_filename = repo_name + ".json"
    cmd = ['./gitleaks-darwin-amd64', '--access-token', API_KEY, '--config', 'rules.toml',
       '--repo', repo_url, '--branch', 'master', '--report', results_filename, '--timeout', '2m']
    p = subprocess.Popen(cmd)
    p.wait()
    if os.path.exists(results_filename):
        leak_repo.append(repo_name)
        unique_filename = repo_name + "_unique.json"
        with open(results_filename) as f:
            Json_Data = json.loads(f.read())
            unique_json = []
            for m in range(0, len(Json_Data)):
                if Json_Data[m]["line"] not in unique_json:
                    unique_json.append(Json_Data[m]["line"])
            f2 = open(unique_filename, "w")
            for y in range(0, len(unique_json)):
                data = unique_json[y].strip()
                f2.write(data)
                f2.write("\n")
            f2.close()

repos.close()


#alerting via slack
Msg2 = "*[+]New leaks found! Repositories :*" + "\n"
if len(leak_repo) > 0:
    #response = client.chat_postMessage(channel=slack_channel, text=Msg2)
    for repo in leak_repo:
        msg3 = "\t\t"+str(repo)
        #response = client.chat_postMessage(channel=slack_channel, text=msg3)
