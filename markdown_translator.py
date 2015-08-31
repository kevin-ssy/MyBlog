import requests
import urllib
import json
import EMailSender
import os
header = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'connection': 'close'}
url = 'http://meta.alibaba-inc.com/store/table/detail/wiki_diff.html?spm=0.0.0.0.N7Qbvj&guid=odps.tbcdm.dim_tb_itm&version=&viewOnLoad=true'
# response = requests.get(url, headers=header)
# res = urllib2.urlopen(url)
# html = response.text
crawl_url = 'http://meta.alibaba-inc.com/simba/odpsMetaTableExt/getWiki?guid=odps.tbcdm.dim_tb_itm&version=79'
header_masquerade = {'Cookie': 'lzstat_uv=38745615742361254760|2758410@3097609@3222887@2988940;'
                               ' c_token=991c2a690c65681b4bdf9310f9d1fd07;'
                               ' ck2=dc8ac9af6b5b5640c722036cfd36faa3;'
                               ' an=kevin.ssy; lg=true; sg=y15; CNZZDATA1000236664=1676365246-1437033655-%7C1440997457;'
                               ' isg=17119C2EC571AC7D46281F6FA355CCB2;'
                               ' l=Aisr/OsKVzjc4nMmjdgi-V3DO0EXnj-c;'
                               ' JSESSIONID=DDB4A8579F2B4761EFE4A85F7BD74B20;'
                               ' lvc=sAmAI%2BLKYv85tQ%3D%3D',
                     'Connection': 'keep-alive',
                     'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

response = requests.get(crawl_url, headers=header_masquerade)
text_json = response.json()
content = text_json[u'data'][u'content']
content = content.encode('utf-8')
# content = urllib.quote(content)
content = content.split('\n')
output = ''
for line in content:
    output = output+line+'\\n'
content = output.split('\t')
output = ''
for line in content:
    output = output+line+'\\t'
content = output.split('\r')
output = ''
for line in content:
    output = output+line+'\\r'
content = output.split('\b')
output = ''
for line in content:
    output = output+line+'\\b'
content = output.split('\f')
output = ''
for line in content:
    output = output+line+'\\f'
content = output.split('&')
output = ''
for line in content:
    output = output+line+'\&'
content = output.split('\'')
output = ''
for line in content:
    output = output+line+"\\\'"
content = output.split('\"')
output = ''
for line in content:
    output = output+line+"\\\""
f = open('temp.js', 'w')
f.write('var md = require(\'markdown-it\')();var result = md.render(\'%s\');'
        'var fs = require(\'fs\');'
        'fs.writeFile(\'temp.txt\',result,function (err) {if (err) throw err;});' % output)
f.close()
command = 'node temp.js'
os.system(command)
fr = open('temp.txt', 'r')
ncontent = fr.read()
fr.close()
EMailSender.send_email(102465, 'icbu', 'CPU OVERLOAD!', 'icbu_ensa_dev'.encode('utf-8'),
                   '20150724085838637gwlgx4sb1'.encode('utf-8'), ncontent, rate=0.653398)
print response.text