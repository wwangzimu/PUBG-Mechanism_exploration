import time
from  header import header,json,requests,os
import xlwt
#本文件用来获取组队形式的玩家数据
#传入参数依次为玩家ID列表，被搜索的玩家，最近14天所玩比赛数量，组队模式
def Team_of_AllPlayer(PlayerID=[],Count_Of_Team=[],count_match=int,Player_Model=int,):
    AllMatches=[]
    Player_IDs = []
    # 本赛季中的最新分段、平均击杀、和平均伤害,带复数的是全部场次数据
    Average_Rank = []#存储每局游戏每位玩家的分段
    Average_Kill = []#存储每局游戏每位玩家的击杀
    Average_Damage = []#存储每局游戏每位玩家的场伤
    Average_Damages_of_Team=[]#存储每局游戏每一队的平均场伤


    print("以分组形式处理全部玩家赛季数据")
    # 需要对玩家名称数组进行分组，决定进行循环几次，并且最后一次循环的数值可能不够10个
    #四排每次仅请求2队玩家，如果是双排每次请求5队玩家
    #通过循环找这次比赛有多少支队伍，即WinPlace最大的
    #队伍数量
    TeamCount=len(Count_Of_Team)
    print('队伍数量为：'+str(TeamCount))
    # 需要拆分的行数为temp行,分奇偶
    if len(PlayerID) %10 ==0:
        temp = int(len(PlayerID) / 10)
    else:
        temp = int(len(PlayerID) / 10) + 1
    for i in range(temp):
        temp_player = []
        for j in range(10):
            # 如果还在玩家列表内
            if ((i * 10 + j) < len(PlayerID)):
                # 先将每行j列数组添加到一个列表中，再把该列表添加到最终的Player_IDs集合，使得Player_IDs最终为temp行玩家，每行最大10个玩家的表现形式
                temp_player.append(PlayerID[i * 10 + j])

        Player_IDs.append(temp_player)
    # 循环的次数有Pleyer_Names有多少行决定
    for k in range(temp):
        # print(str(Player_IDs[k]))
        # 获取玩家2020年第一赛季的统计信息
        if Player_Model == 1:
            PlayersSeasonurl = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-06/gameMode/squad/players?filter[playerIds]='
        elif Player_Model == 2:
            PlayersSeasonurl = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-06/gameMode/squad-fpp/players?filter[playerIds]='
        elif Player_Model == 3:
            PlayersSeasonurl = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-06/gameMode/duo/players?filter[playerIds]='
        else:
            PlayersSeasonurl = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-06/gameMode/duo-fpp/players?filter[playerIds]='
        # print(len(Player_IDs[k]))
        for p in range(len(Player_IDs[k])):
            PlayersSeasonurl = PlayersSeasonurl + str(Player_IDs[k][p])
            if (p != (len(Player_IDs[k]) - 1)):  # 最后一个不用加逗号
                PlayersSeasonurl = PlayersSeasonurl + ','
            else:
                break
        print(PlayersSeasonurl)

        # 获取玩家Matche数据
        # PlayersSeasonurl = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-06/gameMode/squad/players?filter[playerIds]=account.b38fc473d39549d0b454f3c30efcd791'
        PlayersSeason = requests.get(PlayersSeasonurl, headers=header)
        PlayersSeason_requestCode = PlayersSeason.status_code
        if (PlayersSeason_requestCode == 429):
            print("请求太快，请联系作者，或者1min后再尝试")
            break
        if (PlayersSeason_requestCode == 200):
            print('第' + str(count_match) + '场第' + str(k) + '组玩家数据获取成功')
        PlayersSeason_jsondata = json.loads(PlayersSeason.text)
        #print(PlayersSeason_jsondata)
        # 写入赛季信息到txt
        # PlayersSeason_jsondata_txt = open(
        #     os.getcwd() + '/' + str(player_name) + '的全部队友赛季数据' + '第' + str(count_match) + '场第' + str(k + 1) + '组.txt',
        #     'w+', encoding="utf-8")
        # print(PlayersSeason_jsondata, file=PlayersSeason_jsondata_txt)  # 可以使用write的形式，但是write只能写入字符串，不能写入JSON格式，导致不易理解
        # PlayersSeason_jsondata_txt.close()
        #获取到每组的Json后，马上分离出kill、分段、伤害
        # 针对每组中有多少列数据进行处理，避免边界问题
        for q in range(len(Player_IDs[k])):

            # 本赛季中的所有击杀玩家、所有比赛场次、和所有伤害
            if Player_Model == 1:
                All_kills = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad']['kills']
                All_Damages = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad']['damageDealt']
                All_Matches = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad']['roundsPlayed']
                Average_Rank_int = int(
                    PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad']['rankPoints'])
            elif Player_Model == 2:
                All_kills = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad-fpp']['kills']
                All_Damages = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad-fpp'][
                    'damageDealt']
                All_Matches = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad-fpp'][
                    'roundsPlayed']
                Average_Rank_int = int(
                    PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['squad-fpp']['rankPoints'])
            elif Player_Model == 3:
                All_kills = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo']['kills']
                All_Damages = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo']['damageDealt']
                All_Matches = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo']['roundsPlayed']
                Average_Rank_int = int(
                    PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo']['rankPoints'])
            else:
                All_kills = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo-fpp']['kills']
                All_Damages = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo-fpp']['damageDealt']
                All_Matches = PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo-fpp']['roundsPlayed']
                Average_Rank_int = int(
                    PlayersSeason_jsondata['data'][q]['attributes']['gameModeStats']['duo-fpp']['rankPoints'])
            # 出现玩家某场比赛某玩家数据为0的情况,因为有的玩家只玩TPP，有的只玩FPP

            if All_Matches != 0:
                Average_Damage_int = int(All_Damages / All_Matches)
                Average_Kill_float = All_kills / All_Matches

            else:
                Average_Damage_int = 0
                Average_Kill_float = 0
            Average_Kill.append(Average_Kill_float)
            Average_Damage.append(Average_Damage_int)
            Average_Rank.append(Average_Rank_int)
            AllMatches.append(All_Matches)

        time.sleep(10)
    temp=0

   #已经获取到一场比赛内所有玩家的场伤，则根据小队的数量进行获取队伍平均场伤
    for i in range(0,TeamCount):#表示1...N小队循环
        Temp_Damage=0
        UpTeamcout = 0
        # 前面N-1队玩家数量之和
        for j in range(Count_Of_Team[i]):
             Temp_Damage+=Average_Damage[temp+j]
        temp+=Count_Of_Team[i]
        #由于每队玩家的数量已经存储在WinPlacesTeamCount中，因此直接使用该数组中的值计算小队的平均场伤

        if Temp_Damage != 0 :
            Averge_Temp_Damage = int(Temp_Damage / Count_Of_Team[i])  # 注意数组下标对齐
            Average_Damages_of_Team.append(Averge_Temp_Damage)
        else:

            Average_Damages_of_Team.append(0)


    # 该场比赛内玩家
    print(Average_Kill)
    print(Average_Rank)
    print(Average_Damage)
    return Average_Rank,Average_Damage,Average_Kill,Average_Damages_of_Team,AllMatches


