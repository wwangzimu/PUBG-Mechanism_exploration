import json
import requests
from pubg_python import PUBG, Shard
from PIL import Image

VendingMachinecount=0
#打开图片读取数组
im=Image.open('C:/Users/a7385/Desktop/PUBG/测试数据/Miramar_Main_High_Res.png')  #打开图像
pix=im.load()#导入像素

api = PUBG("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhMmZiNjI1MC0wZDQzLTAxMzgtNzE2NS0yZGY4YzdjNjQ2ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTc3NzE4Mjg0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImE3Mzg1MzE1ODItZ21hIn0.ZqMmAbzh-nQbCWUuUuy2I86_CGKqGWyHZvZxVhDe4F0", Shard.PC_AS)


#查询玩家信息
url = "https://api.pubg.com/shards/steam/players?filter[playerNames]=wozuiniuOO"
header = {
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhMmZiNjI1MC0wZDQzLTAxMzgtNzE2NS0yZGY4YzdjNjQ2ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTc3NzE4Mjg0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImE3Mzg1MzE1ODItZ21hIn0.ZqMmAbzh-nQbCWUuUuy2I86_CGKqGWyHZvZxVhDe4F0",
  "Accept": "application/json "

}
Player = requests.get(url, headers=header)

Player_jsondata = json.loads(Player.text)
PlayerID=Player_jsondata['data'][0]['id'] #对中括号部分读取数据需要使用[0]
#print('玩家ID:'+PlayerID)

#获取比赛信息
#根据玩家ID查询比赛的ID
MatchID=[(m['id']) for m in Player_jsondata['data'][0]['relationships']['matches']['data']] #进行for循环
#获得某人批量的匹配URL
MatchURL = [('https://api.pubg.com/shards/steam/matches/' + MatchIDURl) for MatchIDURl in MatchID]
#批量进行请求比赛数据
for matchurl in MatchURL:
    Match = requests.get(matchurl, headers=header)
    Match_jsondata = json.loads(Match.text)
#Match是批量的匹配ID
    #寻找地图及数量
#    print(Match.text)
      # 获取比赛物资的物资下载URL
    for f in Match_jsondata['included'] :
        if f['type']=="asset":
           Match_Telemetry_URL=f['attributes']['URL']

    telemetry = api.telemetry(Match_Telemetry_URL)
#查找饮料机事件
    VendingMachine = telemetry.events_from_type('LogObjectInteraction')
  #vendingmachine.character.location.x是真实坐标，x,y为图片坐标
    for vendingmachine in VendingMachine :
        if vendingmachine.object_type_status == "ACTIVATED":
          # print(vendingmachine.character.location.x)
          # print(vendingmachine.character.location.y)
           #需要强制整形，而且图片分辨率只有坐标的百分之一
            x =int(vendingmachine.character.location.x/100)
            y=int(vendingmachine.character.location.y/100)
            VendingMachinecount=VendingMachinecount+1
            #方圆100像素全部打红
            for i in range(x-10,x+10):
                for j in range(y-10,y+10):
                    pix[i,j] =(255,0,0)
                 #   print(img[x, y])
#循环的次数为渲染点

#plt.figure(VendingMachinecount)
im=im.convert('RGB')
im.save('C:/Users/a7385/Desktop/PUBG/测试数据/test.png')


