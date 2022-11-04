# temp-utility-scripts
temp utility scripts

run gitleaks and get unique secrets detected per repo/service & the original results.

modify rules.toml to include your rules .
modify monitored_repos.txt to add all the repo names to be monitored.
set env var GIT_TOKEN / as dotenv config with github token to access private orgs repos. 
place github binary in the same folder as the script.
>> RUN
