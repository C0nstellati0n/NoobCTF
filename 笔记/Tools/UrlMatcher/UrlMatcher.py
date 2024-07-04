import re
import json
from pathlib import Path
excludeUrls=["www.w3.org/2000/svg","forms.gle","www.twitch.tv","cdn.discordapp.com/emojis","cdn.discordapp.com/avatars","images-ext-1.discordapp.net/external","lh3.googleusercontent.com","cdn.discordapp.com/icons","register","lh4.googleusercontent.com","discord.gg","lh6.googleusercontent.com",".png",".jpg","login","amazonaws.com","tenor.com","wigle.net","dcode.fr","nmap.org","gmail.com",".py","shellcraft.amd64.linux.sh",".gov","picoctf.net","picoctf.org","gchq.github.io/CyberChef","imgur.com","encrypted-tbn0.gstatic.com","pbs.twimg.com","github.com/bata24/gef","pwnable.kr","pwnable.tw","letmegooglethat.com","ibb.co",".tar.gz","webhook.site",".gif"]
bookmarkTemplate="""<DL><p>
    <DT><H3>Writeups</H3>
    <DL><p>
    {}
    </DL><p>
</DL><p>"""
urls=set()
bookmarks=""
def filterUrl(content):
    #https://gist.github.com/gruber/8891611
    urlRe=re.compile(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))")
    match = urlRe.findall(content)
    res=[]
    expect=True
    for i in match:
        expect=True
        for exclude in excludeUrls:
            if exclude in i:
                expect=False
                break
        if expect:
            res.append(i)
    return list(set(res))
def process(path):
    global urls
    global bookmarks
    with open(path,'r') as f:
        content=json.load(f)
    for i in content:
        temp=filterUrl(i['content'])
        if len(temp)!=0:
            for url in temp:
                if not url in urls:
                    bookmarks+=f'<DT><A HREF="{url}">{url}</A>\n'
                    urls.update([url])
path=input("请输入存储所有json文件的文件夹的路径: ")
outputPath=input("请输入结果文件的路径: ")
lastIndex=outputPath.rfind('/')
if lastIndex==-1:
    bookmarksPath=f"bookmarks_{outputPath}"
else:
    bookmarksPath=f"{outputPath[:lastIndex]}/bookmarks_{outputPath[lastIndex+1:]}"
jsons=Path(path).glob("**/*.json")
for jsonFile in jsons:
    process(jsonFile)
with open(bookmarksPath+".html",'w') as f:
    f.write(bookmarkTemplate.format(bookmarks[:-1]))