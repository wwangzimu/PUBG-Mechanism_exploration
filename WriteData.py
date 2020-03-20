from header import time,os,xlwt
def WriteData(All_Average_Rank=[],All_Average_Damage=[],All_Average_Kill=[],All_Average_Damages_of_Team=[],All_Matches=[],All_Count_Of_Team=[],List_Game_time=[],List_Sum_All_Average_Rank=[],List_Sum_All_Average_Kill=[],List_Sum_All_Average_Damage=[],List_Sum_All_Average_Damages_of_Team=[],List_Sum_All_Matches=[],All_player_place=[],player_name=''):
    output_Data_excel = (os.getcwd() + '/' + player_name + '的匹配数据' + time.strftime('%Y-%m-%d', time.localtime(
        time.time())) + '.xls')
    wb = xlwt.Workbook(encoding='utf-8')
    Rank_SheetName = '分段'
    Damage_SheetName = '个人场伤'
    Kill_SheetName = 'KD'
    Damages_of_Team_SheetName = '队伍平均场伤'
    AllMatches_SheetName = '本赛季游戏场数'
    # 用sort方法让数据从小到大排列
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
    All_Matches_Excel = wb.add_sheet(AllMatches_SheetName)

    Rank_Sort_Excel = wb.add_sheet(Rank_Sort_SheetName)
    Damage_Sort_Excel = wb.add_sheet(Damage_Sort_SheetName)
    Kill_Sort_Excel = wb.add_sheet(Kill_Sort_SheetName)
    Damages_of_Team_Sort_Excel = wb.add_sheet(Damages_of_Team_Sort_SheetName)
    All_Matches_Sort_Excel = wb.add_sheet(All_Matches_Sort_SheetName)

    row = 0
    col = 0
    lines = 0;  # 第几行



    colour=[2,3,4,5,6,1]
    # pattern.pattern_fore_colour = 5  # 5 背景颜色为黄色
    # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    # style = xlwt.XFStyle()
    # style.pattern = pattern

    # 写入RANK数据
    # 在写入是对不同队伍间插入空白单元格
    # Newcol=0#Newcol是col添加空白单元格后的新行数，写做col是因为列表中的第几个col表示EXCEL中的第row列，第newcol 数据
    for row in range(len(All_Average_Rank)):  # 读取行循环再列循环
        i = 1
        SumTeamCount = 0
        SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i-1]
        for col in range(len(All_Average_Rank[row])):  # 行列交换转置方便分析
            # 如果写入数据的行数小于前面队伍的和，那么说明还在同一支队伍中，不需要改变样式
            # 统计前面i个队伍数量
            if col >= SumTeamCount:
                i = i + 1
                SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i-1]
                # 设置单元格样式
            #设置单元格样式
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
            # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
            # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray

            style = xlwt.XFStyle()
            style.pattern = pattern
            if All_player_place[row] == i:
                #所处队伍的背景直接改成白色
                #设置白色背景
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern.pattern_fore_colour = colour[5]
                style = xlwt.XFStyle()
                style.pattern = pattern

            Rank_Excel.write(col, row, All_Average_Rank[row][col],style)
            Damage_Excel.write(col, row, All_Average_Damage[row][col],style)
            Kill_Excel.write(col, row, All_Average_Kill[row][col], style)
            All_Matches_Excel.write(col, row, All_Matches[row][col], style)

        Rank_Excel.write(102, row, List_Sum_All_Average_Rank[row],)
        Rank_Excel.write(103, row, List_Game_time[row])
        Damage_Excel.write(102, row, List_Sum_All_Average_Damage[row])
        Damage_Excel.write(103, row, List_Game_time[row])
        All_Matches_Excel.write(102, row, List_Sum_All_Matches[row])
        All_Matches_Excel.write(103, row, List_Game_time[row])
        Kill_Excel.write(102, row, List_Sum_All_Average_Kill[row])
        Kill_Excel.write(103, row, List_Game_time[row])
    # # 写入Damage数据
    # for row in range(len(All_Average_Damage)):  # 读取行循环再列循环
    #     i = 1
    #     SumTeamCount = 0
    #     SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i-1]
    #     for col in range(len(All_Average_Damage[row])):  # 行列交换转置方便分析
    #         # 如果写入数据的行数小于前面队伍的和，那么说明还在同一支队伍中，不需要改变样式
    #         # 统计前面i个队伍数量
    #
    #         if col <= SumTeamCount:
    #             # 设置单元格样式
    #             pattern = xlwt.Pattern()
    #             pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #             pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
    #             # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    #             # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    #             style = xlwt.XFStyle()
    #             style.pattern = pattern
    #
    #         else:
    #             i = i + 1
    #             SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i-1]
    #             pattern = xlwt.Pattern()
    #             pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #             # 如果超过前面玩家队伍之和，说明是下一队的玩家了
    #             pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
    #             # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    #             # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    #             style = xlwt.XFStyle()
    #             style.pattern = pattern
    #          #玩家所处的队伍，单元格颜色不变
    #         if All_player_place[row]!=i:
    #
    #
    #         else:
    #

    # 写入kd数据
    # for row in range(len(All_Average_Kill)):  # 读取行循环再列循环
    #     i = 1
    #     SumTeamCount = 0
    #     SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i - 1]
    #     for col in range(len(All_Average_Kill[row])):  # 行列交换转置方便分析
    #         # 如果写入数据的行数小于前面队伍的和，那么说明还在同一支队伍中，不需要改变样式
    #         # 统计前面i个队伍数量
    #
    #         if col <= SumTeamCount:
    #             # 设置单元格样式
    #             pattern = xlwt.Pattern()
    #             pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #             pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
    #             # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    #             # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    #             style = xlwt.XFStyle()
    #             style.pattern = pattern
    #         else:
    #             i = i + 1
    #             SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i-1]
    #             pattern = xlwt.Pattern()
    #             pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #             # 如果超过前面玩家队伍之和，说明是下一队的玩家了
    #             pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
    #             # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    #             # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    #             style = xlwt.XFStyle()
    #             style.pattern = pattern
    #          #玩家所处的队伍，单元格颜色不变
    #         if i!= All_player_place[row]:
    #             Kill_Excel.write(col, row, All_Average_Kill[row][col], style)
    #         else:
    #             Kill_Excel.write(col, row, All_Average_Kill[row][col])
    #     Kill_Excel.write(102, row, List_Sum_All_Average_Kill[row])
    #     Kill_Excel.write(103, row, List_Game_time[row])
    # 写入队伍平均伤害数据
    for row in range(len(All_Average_Damages_of_Team)):  # 读取行循环再列循环1
        for col in range(len(All_Average_Damages_of_Team[row])):  # 行列交换转置方便分析

            Damages_of_Team_Excel.write(col, row, All_Average_Damages_of_Team[row][col])

        Damages_of_Team_Excel.write(102, row, List_Sum_All_Average_Damages_of_Team[row])
        Damages_of_Team_Excel.write(103, row, List_Game_time[row])
    # 写入游戏场数
    # for row in range(len(All_Matches)):  # 读取行循环再列循环
    #     i = 1
    #     SumTeamCount = 0
    #     SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i-1]
    #     for col in range(len(All_Matches[row])):  # 行列交换转置方便分析
    #         # 如果写入数据的行数小于前面队伍的和，那么说明还在同一支队伍中，不需要改变样式
    #         # 统计前面i个队伍数量
    #
    #
    #         if col <= SumTeamCount:
    #             # 设置单元格样式
    #             pattern = xlwt.Pattern()
    #             pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #             pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
    #             # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    #             # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    #             style = xlwt.XFStyle()
    #             style.pattern = pattern
    #
    #         else:
    #             i = i + 1
    #             SumTeamCount = SumTeamCount + All_Count_Of_Team[row][i - 1]
    #             pattern = xlwt.Pattern()
    #             pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #             # 如果超过前面玩家队伍之和，说明是下一队的玩家了
    #             pattern.pattern_fore_colour = colour[i % 5]  # 使用取余的原因是因为颜色的列表只有21个
    #             # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    #             # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    #
    #             style = xlwt.XFStyle()
    #             style.pattern = pattern
    #          #玩家所处的队伍，单元格颜色不变
    #         if i!= All_player_place[row]:
    #             All_Matches_Excel.write(col, row, All_Matches[row][col], style)
    #         else:
    #             All_Matches_Excel.write(col, row, All_Matches[row][col])
    #     All_Matches_Excel.write(102, row, List_Sum_All_Matches[row])
    #     All_Matches_Excel.write(103, row, List_Game_time[row])
    # 写入Rank顺序
    for row in range(len(All_Average_Rank)):  # 读取行循环再列循环
        All_Average_Rank[row].sort()
        for col in range(len(All_Average_Rank[row])):  # 行列交换转置方便分析
            Rank_Sort_Excel.write(col, row, All_Average_Rank[row][col])
        Rank_Sort_Excel.write(102, row, List_Sum_All_Average_Rank[row])
        Rank_Sort_Excel.write(103, row, List_Game_time[row])

    # 写入Damage数据顺序
    for row in range(len(All_Average_Damage)):  # 读取行循环再列循环
        All_Average_Damage[row].sort()
        for col in range(len(All_Average_Damage[row])):  # 行列交换转置方便分析
            Damage_Sort_Excel.write(col, row, All_Average_Damage[row][col])
        Damage_Sort_Excel.write(102, row, List_Sum_All_Average_Damage[row])
        Damage_Sort_Excel.write(103, row, List_Game_time[row])
    # 写入kd数据顺序
    for row in range(len(All_Average_Kill)):  # 读取行循环再列循环
        All_Average_Kill[row].sort()
        for col in range(len(All_Average_Kill[row])):  # 行列交换转置方便分析
            Kill_Sort_Excel.write(col, row, All_Average_Kill[row][col])
        Kill_Sort_Excel.write(102, row, List_Sum_All_Average_Kill[row])
        Kill_Sort_Excel.write(103, row, List_Game_time[row])
    # 写入队伍平均伤害数据顺序
    for row in range(len(All_Average_Damages_of_Team)):  # 读取行循环再列循环
        All_Average_Damages_of_Team[row].sort()
        for col in range(len(All_Average_Damages_of_Team[row])):  # 行列交换转置方便分析
            Damages_of_Team_Sort_Excel.write(col, row,
                                             All_Average_Damages_of_Team[row][col])
        Damages_of_Team_Sort_Excel.write(102, row, List_Sum_All_Average_Damages_of_Team[row])
        Damages_of_Team_Sort_Excel.write(103, row, List_Game_time[row])
    # 写入游戏场数顺序
    for row in range(len(All_Matches)):  # 读取行循环再列循环
        All_Matches[row].sort()
        for col in range(len(All_Matches[row])):  # 行列交换转置方便分析
            All_Matches_Sort_Excel.write(col, row, All_Matches[row][col])
        All_Matches_Sort_Excel.write(102, row, List_Sum_All_Matches[row])
        All_Matches_Sort_Excel.write(103, row, List_Game_time[row])
    # 关闭文件
    try:
        wb.save(output_Data_excel)
    except :
        output_Data_excel = (os.getcwd() + '/' + player_name + '的匹配数据' + time.strftime('%Y-%m-%d', time.localtime()) + '.xls')
        wb.save(output_Data_excel)
    # 后面不再执行
    print("玩家数据获取完成，请在本软件目录下查看Excle文件")