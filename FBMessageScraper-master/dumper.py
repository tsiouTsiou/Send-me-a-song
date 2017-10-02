import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO

__author__ = "Raghav Sood"
__copyright__ = "Copyright 2014"
__credits__ = ["Raghav Sood"]
__license__ = "CC"
__version__ = "1.0"
__maintainer__ = "Raghav Sood"
__email__ = "raghavsood@appaholics.in"
__status__ = "Production"

if len(sys.argv) <= 1:
	print "Usage:\n 	python dumper.py [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
	print "Example conversation with Raghav Sood"
	print "	python dumper.py 1075686392 2000 0"
	sys.exit()

error_timeout = 30 # Change this to alter error timeout (seconds)
general_timeout = 7 # Change this to alter waiting time afetr every request (seconds)
messages = []
talk = sys.argv[1]
offset = int(sys.argv[3]) if len(sys.argv) >= 4 else int("0")
messages_data = "lolno"
end_mark = "\"payload\":{\"end_of_history\""
limit = int(sys.argv[2])
headers = {"origin": "https://www.facebook.com", 
"accept-encoding": "gzip,deflate", 
"accept-language": "en-US,en;q=0.8", 
"cookie": "fr=0VNFwSk7mmfu2u7Jj.AWV4-up70Vgf8tiP49k34knsSbY.BYgPb5.Lj.FnK.0.0.BZys3d.AWVeu95w; datr=NTaBWJAIP87YHNVUwKSlTpbQ; sb=OTaBWMJNmNEnZ6Cw3YmE9BZS; c_user=100008086594762; xs=24%3AvAmxfeNPDbyiFQ%3A2%3A1491924430%3A1985%3A7220; wd=1760x302; act=1506463407142%2F1; presence=EDvF3EtimeF1506463554EuserFA21B08086594762A2EstateFDutF1506463554081CEchFDp_5f1B08086594762F11CC; pnl_data2=eyJhIjoiQmlnUGlwZS9pbml0IiwiYyI6IlhGYWNlYm9va01lc3NlbmdlckluYm94Q29udHJvbGxlciIsImIiOmZhbHNlLCJkIjoiL21lc3NhZ2VzL3QvbGluZGEueHguNzEiLCJlIjpbXX0%3D", 
"pragma": "no-cache", 
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36", 
"content-type": "application/x-www-form-urlencoded", 
"accept": "*/*", 
"cache-control": "no-cache", 
"referer": "https://www.facebook.com/messages/zuck"}

base_directory = "Messages/"
directory = base_directory + str(talk) + "/"
pretty_directory = base_directory + str(talk) + "/Pretty/"

try:
	os.makedirs(directory)
except OSError:
	pass # already exists

try:
	os.makedirs(pretty_directory)
except OSError:
	pass # already exists

while end_mark not in messages_data:

	data_text = {"messages[user_ids][" + str(talk) + "][offset]": str(offset), 
	"messages[user_ids][" + str(talk) + "][limit]": str(limit), 
	"client": "web_messenger", 
	"__user": "100008086594762", 
	"__a": "1", 
	"__dyn": "7AgNeS-aF398jgDxyIGzGomzEbHGiWF3oyejrWo466ES2N6wAxu13wFGEa8Gm4UJi28rxuF98qDKuEjKexKui4GVk3ucDBxe6ohyVeFFUkxvxOcG4K5o5aayrgS2m4oqyUfe5FHxu9gqxKVUoh8CrxqdCUmyE9VQm5Eeo4e9Dx6WK6pESfyaBy8OcxO12zVolyoK7UyUhUF3bDwgXiy6bzef-EqBx67byUmzUyh0", 
	"__req": "g", 
	"fb_dtsg": "AQEAjCbDojfT:AQG4dqSrrX6-", 
	"ttstamp": "1506463112119", 
	"__rev": "3326321"}
	data = urllib.urlencode(data_text)
	url = "https://www.facebook.com/ajax/mercury/thread_info.php"
	
	print "Retrieving messages " + str(offset) + "-" + str(limit+offset) + " for conversation ID " + str(talk)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	compressed = StringIO.StringIO(response.read())
	decompressedFile = gzip.GzipFile(fileobj=compressed)
	
	
	outfile = open(directory + str(offset) + "-" + str(limit+offset) + ".json", 'w')
	messages_data = decompressedFile.read()
	messages_data = messages_data[9:]
	json_data = json.loads(messages_data)
	if json_data is not None and json_data['payload'] is not None:
		try:
			messages = messages + json_data['payload']['actions']
		except KeyError:
			pass #no more messages
	else:
		print "Error in retrieval. Retrying after " + str(error_timeout) + "s"
		print "Data Dump:"
		print json_data
		time.sleep(error_timeout)
		continue
	outfile.write(messages_data)
	outfile.close()	
	command = "python -mjson.tool " + directory + str(offset) + "-" + str(limit+offset) + ".json > " + pretty_directory + str(offset) + "-" + str(limit+offset) + ".pretty.json"
	os.system(command)
	offset = offset + limit
	time.sleep(general_timeout) 

finalfile = open(directory + "complete.json", 'wb')
finalfile.write(json.dumps(messages))
finalfile.close()
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
os.system(command)
