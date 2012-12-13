#!/usr/bin/python
import requests
import json
import sys

def color(val):
	if val == True:
		return '\033[92m' + str(val) + '\033[0m'
	elif val == False:
		return '\033[91m' + str(val) + '\033[0m'

def repo_list(repos, token):
	for repo in repos:
		print repo['full_name']
		print '\t Issues Enabled' + color(repo['has_issues'])
		print '\t Wiki Enabled: ' + color(repo['has_wiki'])
		print '\t Downloads Enabled: ' + color(repo['has_downloads'])	

def repo_update(repos, token):
	for repo in repos:
		if sys.argv[4].lower() != str(repo[sys.argv[3]]).lower():
			#print sys.argv[4] + " = " + str(repo[sys.argv[3]])
			json_upd = { 'name' : repo['name'], sys.argv[3] : sys.argv[4] }
			print json_upd
			#print json_upd
			repo_upd = requests.post(repo['url'] + token, data=json.dumps(json_upd))
			print repo_upd.text
			print repo['full_name'] + " Updated"

def hook_list(repos, token):
	for repo in repos:
		print repo['name']
		list_hook = requests.get(repo['url'] + "/hooks" + token)
		print list_hook.text

def hook_update(repos, token):
	for repo in repos:
		print repo['name']
		list_hook = requests.get(repo['url'] + "/hooks" + token)
		#print list_hook.text

		args = dict([arg.split('=', 1) for arg in sys.argv[4:]])
		json_upd = { 'name': sys.argv[3], 'active': True, 'config': args }
		if json.loads(list_hook.text):
			for hook in json.loads(list_hook.text):
				#print json_upd
				if hook['name'] == sys.argv[3] :
					hook_upd = requests.post(hook['url'] + token, data=json.dumps(json_upd))
		else:
			hook_upd = requests.post(repo['url'] + "/hooks" + token, data=json.dumps(json_upd))
		print "\t" + hook_upd.text



print sys.argv
api = "https://api.github.com"
org = ""
token = "?access_token="
repos = requests.get(api + "/orgs/" + org + "/repos" + token)
reposj = json.loads(repos.text)
#print reposj[0]["url"]


funcs = {
#    'CONNECT': connect,
	'repolist': repo_list,
	'repoupdate': repo_update,
	'hooklist': hook_list,
	'hookupdate': hook_update
}
funcs[sys.argv[1]+sys.argv[2]](reposj, token)