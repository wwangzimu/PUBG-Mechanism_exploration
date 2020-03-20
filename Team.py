import xlwt

from header import header, json, requests, os
# from PlayersSeansonStatistics import PlayerSeasonStatics
from Team_of_AllPlayers import Team_of_AllPlayer
from WriteData import WriteData
from  Telemetry_Deal import Telemetry_Deal
import time

# from PlayerLifeStatics import PlayerLifeStatics
# from pubg_python import PUBG, Shard
# 框架：获取自身ID,获取队友ID及战绩，再获取所有对局成员的ID及战绩
# api = PUBG("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhMmZiNjI1MC0wZDQzLTAxMzgtNzE2NS0yZGY4YzdjNjQ2ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTc3NzE4Mjg0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImE3Mzg1MzE1ODItZ21hIn0.ZqMmAbzh-nQbCWUuUuy2I86_CGKqGWyHZvZxVhDe4F0", Shard.PC_AS)
# 获取玩家比赛数据
# players = api.players().filter(player_names=['wan_zimu'])

All_Average_Rank = []  # 存储一位玩家最近14天所有玩家的分段
All_Average_Damage = []  # 存储一位玩家最近14天所有玩家的场伤
All_Average_Kill = []  # 存储一位玩家最近14天所有玩家的击杀
All_Average_Damages_of_Team = []  # 存储一位玩家最近14天所有对局的所有队伍平均场伤，一行表示一队平均场伤
All_Matches = []  # 存储一位玩家最近14天所有玩家的本赛季游戏场数
All_Count_Of_Team = []  # 存储一位玩家最近14天所有玩家不同队伍的队员数量
All_Telemetry_Item_ID=[] #存储一位玩家最近14天所有玩家不同队伍的队员ID
#游戏时间列表
List_Game_time=[]
# 平均值列表
List_Sum_All_Average_Rank = []
List_Sum_All_Average_Damage = []
List_Sum_All_Average_Kill = []
List_Sum_All_Average_Damages_of_Team = []
List_Sum_All_Matches = []

#玩家最近场游戏中的排名
All_player_place=[]
#每场只需要获取一次
print("绝地求生组队分析小工具 作者：小黑盒ID:10351265,QQ群：201359150")
print("请输入你的ID,区分大小写，确认按回车键")

# 获取Matches的数据并写入Player_jsondata_txt
#
# 此处要做输入错误校准
#
while (1):

    player_name = input()
    #player_name='wan_zimu'
    print("请输入组队的模式，四排TPP输入数字1，四排FPP输入数字2,双排TPP输入数字3，双排FPP输入数字4")
    while (1):
        Player_Model = int(input())
        #Player_Model=1
        if Player_Model == 1 or Player_Model == 2 or Player_Model == 3 or Player_Model == 4:
            # print("输入游戏的时间")
            # Play_Time = input()
            break
        else:
            print("输入不对，请重新输入")

    # 拼凑链接
    url = 'https://api.pubg.com/shards/steam/players?filter[playerNames]=' + player_name
    # url = 'https://api.pubg.com/shards/steam/players?filter[playerNames]=NiWeihanii'
    # url = 'https://api.pubg.com/shards/steam/players?filter[playerIds]=wan_zimu'
    # 获取玩家Matche数据
    Player = requests.get(url, headers=header)
    Player_jsondata_requestCode = Player.status_code
    print(Player_jsondata_requestCode)
    if (Player_jsondata_requestCode == 200):
        break
    if (Player_jsondata_requestCode == 429):
        print("向服务器请求次数太多，请等30后再输入ID")
    print("输入ID不正确，请重新输入")
print("输入成功,请等待")
print("开始获取玩家数据")
# 打开与关闭文件Player_jsondata_txt
# PUBG的JSON中NONE需要改为"NONE"才能用JSON解析工具打开
Player_jsondata_txt = open(os.getcwd() + '\Player_jsondata.txt', 'w+', encoding="utf-8")
Player_jsondata = json.loads(Player.text)
print(Player_jsondata, file=Player_jsondata_txt)  # 可以使用write的形式，但是write只能写入字符串，不能写入JSON格式，导致不易理解
Player_jsondata_txt.close()
Player_jsondata_txt_read = open(os.getcwd() + '\Player_jsondata.txt', 'r', encoding="utf-8")
Player_NONE = Player_jsondata_txt_read.read()  # Player_NONE是需要替换的NONE
t = Player_NONE.replace("None", '"None"')  # 注意要转义

Player_jsondata_txt_write = open(os.getcwd() + '\Player_jsondata.txt', 'w+', encoding="utf-8")
print(t, file=Player_jsondata_txt_write)  # 可以使用write的形式，但是write只能写入字符串，不能写入JSON格式，导致不易理解
Player_jsondata_txt_read.close()
Player_jsondata_txt_write.close()
# print输出到txt


# 使用for获取14天所有比赛的MatchID，并获取每场比赛的详细数据
MatchID = Player_jsondata['data'][0]['id']  # 对中括号部分读取数据需要使用[0]
print("玩家账号ID获取成功")
# 获取比赛信息
# 根据玩家ID查询比赛的ID
MatchID = [(m['id']) for m in Player_jsondata['data'][0]['relationships']['matches']['data']]  # 进行for循环

# 获得某人批量的匹配URL
MatchURL = [('https://api.pubg.com/shards/steam/matches/' + MatchIDURl) for MatchIDURl in MatchID]
print('一共有' + str(len(MatchURL)) + '场数据需要处理')

count_match = 0  # 数正在处理第几场比赛用
# 批量进行请求比赛数据
for matchurl in MatchURL:
    Match = requests.get(matchurl, headers=header)

    # PUBG的JSON中NONE需要改为"NONE"才能用JSON解析工具打开,但是不处理不影响代码的读取
    # 打开与关闭文件Player_jsondata_txt
    Match_jsondata_txt = open(os.getcwd() + '\Match_jsondata.txt', 'w+', encoding="utf-8")
    Match_jsondata = json.loads(Match.text)
    print(Match_jsondata, file=Match_jsondata_txt)  # 可以使用write的形式，但是write只能写入字符串，不能写入JSON格式，导致不易理解
    Match_jsondata_txt.close()
    # 先保存文本，保存后用对象1读取，再用对象2保存，不能用同一个对象

    Match_jsondata_txt_read = open(os.getcwd() + '\Match_jsondata.txt', 'r', encoding="utf-8")
    Match_NONE = Match_jsondata_txt_read.read()  # Match_NONE是需要替换的NONE
    t = Match_NONE.replace("None", "\"None\"")  # 注意要转义

    Match_jsondata_txt_write = open(os.getcwd() + '\Match_jsondata.txt', 'w+', encoding="utf-8")
    print(t, file=Match_jsondata_txt_write)  # 可以使用write的形式，但是write只能写入字符串，不能写入JSON格式，导致不易理解
    Match_jsondata_txt_read.close()
    Match_jsondata_txt_write.close()
    #print(t)
    # print输出到txt
    Match_jsondata_txt.close()
    # 由于Include字段包括资源以及其他干扰项，因此需要将其分离
    PlayersNames = []  #
    PlayerIDs = []  # 一场比赛中所有玩家ID是一个数组

    PlayerCount = 0
    # 在循环时不仅获取玩家的ID、名称、还获取玩家排名WinPlace
    for Include in Match_jsondata['included']:
        if Include['type'] == "asset":
           Telemetry_URL = Include['attributes']['URL']
           break

    # 获取某场比赛中所有玩家ID成功，需要将玩家ID、KD、分段、所有比赛场次等写入EXCEL中分析

    # PlayerSeasonStatics(PlayerIDs,str(player_names),count_match,Player_Model)

    #清空接受列表
    List_Telemetry_Item_Nanme=[]
    Count_Of_Team=[]
    List_Telemetry_Item_ID=[]
    player_place=0
    (List_Telemetry_Item_Name,Count_Of_Team,PlayerID,player_place)=Telemetry_Deal(Telemetry_URL,player_name)
    # 只获取最近X场数据，由count_match控制
    if count_match < 10:
        # 统计比赛场次
        count_match += 1
        # 清空接受队列
        Average_Rank = []
        Average_Damage = []
        Average_Kill = []
        Average_Damages_of_Team = []
        AllMatches=[]
        #调用外部文件的方法对玩家赛季数据进行处理
        (Average_Rank, Average_Damage, Average_Kill, Average_Damages_of_Team,AllMatches) = Team_of_AllPlayer(PlayerID,Count_Of_Team,  count_match, Player_Model)
        All_Average_Rank.append(Average_Rank)
        All_Average_Damage.append(Average_Damage)
        All_Average_Kill.append(Average_Kill)
        All_Average_Damages_of_Team.append(Average_Damages_of_Team)
        All_Matches.append(AllMatches)
        All_Count_Of_Team.append(Count_Of_Team)


        All_player_place.append(player_place)


        Sum_All_Average_Rank=0
        Sum_All_Average_Damage=0
        Sum_All_Average_Kill=0
        Sum_All_Average_Damages_of_Team=0
        Sum_All_Matches=0

        #把每张表的每局比赛的平均值写成一个列表，虽然可以在最后对列表进行统计，但是懒得那么做

        print('本场比赛玩家数量：' + str(PlayerCount))
        print(PlayersNames)
        print(All_Average_Rank)
        print(All_Average_Damage)
        print(All_Average_Kill)
        print(All_Average_Damages_of_Team)
        # 对单场此赛求平均值,不想使用np,应该写成方法的，但是这次算了
        for temp in Average_Rank:
            Sum_All_Average_Rank += temp
        for temp in Average_Damage:
            Sum_All_Average_Damage += temp
        for temp in Average_Kill:
            Sum_All_Average_Kill +=temp
        for temp in Average_Damages_of_Team:
            Sum_All_Average_Damages_of_Team += temp
        for temp in AllMatches:
            Sum_All_Matches += temp
        #每局比赛的平均分
        List_Sum_All_Average_Rank.append(Sum_All_Average_Rank/len(Average_Rank))
        List_Sum_All_Average_Kill.append(Sum_All_Average_Kill/len(Average_Damage))
        List_Sum_All_Average_Damage.append(Sum_All_Average_Damage/len(Average_Kill))
        List_Sum_All_Average_Damages_of_Team.append(Sum_All_Average_Damages_of_Team/len(Average_Damages_of_Team))
        List_Sum_All_Matches.append(Sum_All_Matches/len(AllMatches))
        #每局比赛的时间
        Game_Time = Match_jsondata['data']['attributes']['createdAt']
        NewGame_Time = ""
        for a in range(len(Game_Time)):
            if a == 11:
                h = int(Game_Time[11] + Game_Time[12]) + 8
                if (h >= 24):
                    h = h - 24
                if (h < 10):
                    NewGame_Time = NewGame_Time + '0'
                NewGame_Time = NewGame_Time + str(h)
                print(h)
                continue
            if a == 12:
                continue
            #只要小时和分钟
            if a>=11 :
                NewGame_Time = NewGame_Time + Game_Time[a]
            if a == 15:
                break
        List_Game_time.append(NewGame_Time)

    else:
        WriteData(All_Average_Rank, All_Average_Damage, All_Average_Kill, All_Average_Damages_of_Team, All_Matches,
                  All_Count_Of_Team, List_Game_time,List_Sum_All_Average_Rank,List_Sum_All_Average_Kill,List_Sum_All_Average_Damage,List_Sum_All_Average_Damages_of_Team,List_Sum_All_Matches,All_player_place,player_name)

        break