import xlwt

from header import header, json, requests, os
# from PlayersSeansonStatistics import PlayerSeasonStatics
from Team_of_AllPlayers import Team_of_AllPlayer
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
All_Matches=[]#存储一位玩家最近14天所有玩家的本赛季游戏场数
print("绝地求生组队分析小工具 作者：小黑盒ID:10351265,QQ群：201359150")
print("请输入你的ID,区分大小写，确认按回车键")

# 获取Matches的数据并写入Player_jsondata_txt
#
# 此处要做输入错误校准
#
while (1):

    player_name = input()
    print("请输入组队的模式，四排TPP输入数字1，四排FPP输入数字2,双排TPP输入数字3，双排FPP输入数字4")
    while (1):
        Player_Model = int(input())
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
print(t)
# print输出到txt


# 使用for获取14天所有比赛的MatchID，并获取每场比赛的详细数据
MatchID = Player_jsondata['data'][0]['id']  # 对中括号部分读取数据需要使用[0]
print("玩家单场比赛ID获取成功")
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
    Player_Win_Places = []  # 一场比赛中所有玩家的排名，与PlayerIDs一一对应

    PlayerCount = 0
    # 在循环时不仅获取玩家的ID、名称、还获取玩家排名WinPlace
    for Include in Match_jsondata['included']:
        # print(Include)
        if str(Include['type']) == 'participant':
            PlayersNames.append(Include['attributes']['stats']['name'])
            PlayerIDs.append(Include['attributes']['stats']['playerId'])
            Player_Win_Places.append(Include['attributes']['stats']['winPlace'])
            # AllMatches.append(Include['attributes']['stats']['roundsPlayed'])
            PlayerCount += 1
        # PlayerIDs.append(str(Include['type']))
    # print(PlayerIDs)
    # 获取某场比赛中所有玩家ID成功，需要将玩家ID、KD、分段、所有比赛场次等写入EXCEL中分析

    # PlayerSeasonStatics(PlayerIDs,str(player_names),count_match,Player_Model)

    # 只获取最近X场数据，由count_match控制
    if count_match < 1:
        # 统计比赛场次
        count_match += 1
        # 清空接受队列
        Average_Rank = []
        Average_Damage = []
        Average_Kill = []
        Average_Damages_of_Team = []
        AllMatches=[]
        #调用外部文件的方法对玩家赛季数据进行处理
        (Average_Rank, Average_Damage, Average_Kill, Average_Damages_of_Team,AllMatches) = Team_of_AllPlayer(PlayerIDs,
                                                                                                  Player_Win_Places,
                                                                                                  str(player_name),
                                                                                                  count_match,
                                                                                                  Player_Model)
        All_Average_Rank.append(Average_Rank)
        All_Average_Damage.append(Average_Damage)
        All_Average_Kill.append(Average_Kill)
        All_Average_Damages_of_Team.append(Average_Damages_of_Team)
        All_Matches.append(AllMatches)
        print('本场比赛玩家数量：' + str(PlayerCount))
        print(PlayersNames)
        print(All_Average_Rank)
        print(All_Average_Damage)
        print(All_Average_Kill)
        print(All_Average_Damages_of_Team)
        # 列表写入的excel文件output_excel
        # output_All_Average_Rank_excel=(os.getcwd()+'/'+player_name+'的分段表'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.xls')
        # output_All_Average_Damage_excel = (os.getcwd() + '/' + player_name + '的分段表' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.xls')
        # output_All_Average_Kill_excel=(os.getcwd()+'/'+player_name+'的分段表'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.xls')
        # output_All_Average_Damages_of_Team_excel=(os.getcwd()+'/'+player_name+'的分段表'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.xls')
        output_Data_excel = (os.getcwd() + '/' + player_name + '的匹配数据' + time.strftime('%Y-%m-%d', time.localtime(
            time.time())) + '.xls')
        wb = xlwt.Workbook(encoding='utf-8')
        Rank_SheetName = '分段'
        Damage_SheetName = '个人场伤'
        Kill_SheetName = 'KD'
        Damages_of_Team_SheetName = '队伍平均场伤'
        AllMatches_SheetName='本赛季游戏场数'
       #用sort方法让数据从小到大排列
        Rank_Sort_SheetName = '分段顺序'
        Damage_Sort_SheetName = '个人场伤顺序'
        Kill_Sort_SheetName = 'KD顺序'
        Damages_of_Team_Sort_SheetName = '队伍平均场伤顺序'
        All_Matches_Sort_SheetName = '本赛季游戏场数顺序'
        # 添加10张表
        Rank_Excel = wb.add_sheet(Rank_SheetName)
        Damage_Excel = wb.add_sheet(Damage_SheetName)
        Kill_Excel = wb.add_sheet(Kill_SheetName)
        Damages_of_Team_Excel = wb.add_sheet(Damages_of_Team_SheetName)
        All_Matches_Excel=wb.add_sheet(AllMatches_SheetName)

        Rank_Sort_Excel = wb.add_sheet(Rank_Sort_SheetName)
        Damage_Sort_Excel = wb.add_sheet(Damage_Sort_SheetName)
        Kill_Sort_Excel = wb.add_sheet(Kill_Sort_SheetName)
        Damages_of_Team_Sort_Excel = wb.add_sheet(Damages_of_Team_Sort_SheetName)
        All_Matches_Sort_Excel = wb.add_sheet(All_Matches_Sort_SheetName)

        row = 0
        col = 0
        lines = 0;  # 第几行
        # 写入RANK数据
        for row in range(len(All_Average_Rank)):  # 读取行循环再列循环
            for col in range(len(All_Average_Rank[row])):  # 行列交换转置方便分析
                Rank_Excel.write(col, row, All_Average_Rank[row][col])
        # 写入Damage数据
        for row in range(len(All_Average_Damage)):  # 读取行循环再列循环
            for col in range(len(All_Average_Damage[row])):  # 行列交换转置方便分析
                Damage_Excel.write(col, row, All_Average_Damage[row][col])
        # 写入kd数据
        for row in range(len(All_Average_Kill)):  # 读取行循环再列循环
            for col in range(len(All_Average_Kill[row])):  # 行列交换转置方便分析
                Kill_Excel.write(col, row, All_Average_Kill[row][col])
        # 写入队伍平均伤害数据
        for row in range(len(All_Average_Damages_of_Team)):  # 读取行循环再列循环
            for col in range(len(All_Average_Damages_of_Team[row])):  # 行列交换转置方便分析
                Damages_of_Team_Excel.write(col, row,
                                 All_Average_Damages_of_Team[row][col])
        # 写入游戏场数
        for row in range(len(All_Matches)):  # 读取行循环再列循环
            for col in range(len(All_Matches[row])):  # 行列交换转置方便分析
                All_Matches_Excel.write(col, row,All_Matches[row][col])
        #进行sort排序，排序后列表名称一样
        # All_Average_Rank.sort()
        # All_Average_Damage.sort()
        # All_Average_Kill.sort()
        # All_Average_Damages_of_Team.sort()
        # All_Matches.sort()
        # 写入RANK数据顺序
        for row in range(len(All_Average_Rank)):  # 读取行循环再列循环
            All_Average_Rank[row].sort()
            for col in range(len(All_Average_Rank[row])):  # 行列交换转置方便分析
                Rank_Sort_Excel.write(col, row, All_Average_Rank[row][col])
        # 写入Damage数据顺序
        for row in range(len(All_Average_Damage)):  # 读取行循环再列循环
            All_Average_Damage[row].sort()
            for col in range(len(All_Average_Damage[row])):  # 行列交换转置方便分析
                Damage_Sort_Excel.write(col, row, All_Average_Damage[row][col])
        # 写入kd数据顺序
        for row in range(len(All_Average_Kill)):  # 读取行循环再列循环
            All_Average_Kill[row].sort()
            for col in range(len(All_Average_Kill[row])):  # 行列交换转置方便分析
                Kill_Sort_Excel.write(col, row, All_Average_Kill[row][col])
        # 写入队伍平均伤害数据顺序
        for row in range(len(All_Average_Damages_of_Team)):  # 读取行循环再列循环
            All_Average_Damages_of_Team[row].sort()
            for col in range(len(All_Average_Damages_of_Team[row])):  # 行列交换转置方便分析
                Damages_of_Team_Sort_Excel.write(col, row,
                                            All_Average_Damages_of_Team[row][col])
        # 写入游戏场数顺序
        for row in range(len(All_Matches)):  # 读取行循环再列循环
            All_Matches[row].sort()
            for col in range(len(All_Matches[row])):  # 行列交换转置方便分析
                All_Matches_Sort_Excel.write(col, row, All_Matches[row][col])

        # 关闭文件


        wb.save(output_Data_excel)
        #后面不再执行
    else:
        print("玩家数据获取完成，请在本软件目录下查看Excle文件")
        break