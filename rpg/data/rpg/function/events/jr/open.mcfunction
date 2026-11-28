# 旅程页的数值 → storage rpg:events v（面板页都是这样拼字的）
scoreboard players add @s rpg_bt_total 0
data modify storage rpg:events v set value {n:"",x:0,z:0,left:0}
data modify storage rpg:events v.n set from storage rpg:events cur.n
data modify storage rpg:events v.x set from storage rpg:events cur.x
data modify storage rpg:events v.z set from storage rpg:events cur.z
execute store result storage rpg:events v.left int 1 run scoreboard players get #left rpg_ev
execute store result storage rpg:events v.total int 1 run scoreboard players get @s rpg_bt_total
scoreboard players add @s rpg_bt_p1 0
execute store result storage rpg:events v.p1 int 1 run scoreboard players get @s rpg_bt_p1
scoreboard players add @s rpg_bt_p2 0
execute store result storage rpg:events v.p2 int 1 run scoreboard players get @s rpg_bt_p2
scoreboard players add @s rpg_bt_p3 0
execute store result storage rpg:events v.p3 int 1 run scoreboard players get @s rpg_bt_p3
data modify storage rpg:events v merge value {home:"（还没有）",fac:"教廷",rep:0,bn:0,tn:0,pt:0}
execute if entity @s[tag=rpg.dm] run data modify storage rpg:events v.fac set value "恶魔"
execute if score @s rpg_tw_home matches 1 run data modify storage rpg:events v.home set value "伯利恒"
execute if score @s rpg_tw_home matches 1 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_1
execute if score @s rpg_tw_home matches 2 run data modify storage rpg:events v.home set value "撒玛利亚"
execute if score @s rpg_tw_home matches 2 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_2
execute if score @s rpg_tw_home matches 3 run data modify storage rpg:events v.home set value "波斯拉"
execute if score @s rpg_tw_home matches 3 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_3
execute if score @s rpg_tw_home matches 4 run data modify storage rpg:events v.home set value "底本"
execute if score @s rpg_tw_home matches 4 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_4
execute if score @s rpg_tw_home matches 5 run data modify storage rpg:events v.home set value "拉巴"
execute if score @s rpg_tw_home matches 5 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_5
execute if score @s rpg_tw_home matches 6 run data modify storage rpg:events v.home set value "迦特"
execute if score @s rpg_tw_home matches 6 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_6
execute if score @s rpg_tw_home matches 7 run data modify storage rpg:events v.home set value "哈马"
execute if score @s rpg_tw_home matches 7 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_7
execute if score @s rpg_tw_home matches 8 run data modify storage rpg:events v.home set value "西顿"
execute if score @s rpg_tw_home matches 8 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_8
execute if score @s rpg_tw_home matches 9 run data modify storage rpg:events v.home set value "拉末"
execute if score @s rpg_tw_home matches 9 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_9
execute if score @s rpg_tw_home matches 10 run data modify storage rpg:events v.home set value "伯大尼"
execute if score @s rpg_tw_home matches 10 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_10
execute if score @s rpg_tw_home matches 11 run data modify storage rpg:events v.home set value "希伯仑"
execute if score @s rpg_tw_home matches 11 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_11
execute if score @s rpg_tw_home matches 12 run data modify storage rpg:events v.home set value "示剑"
execute if score @s rpg_tw_home matches 12 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_12
execute if score @s rpg_tw_home matches 13 run data modify storage rpg:events v.home set value "提幔"
execute if score @s rpg_tw_home matches 13 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_13
execute if score @s rpg_tw_home matches 14 run data modify storage rpg:events v.home set value "基珥"
execute if score @s rpg_tw_home matches 14 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_14
execute if score @s rpg_tw_home matches 15 run data modify storage rpg:events v.home set value "雅谢"
execute if score @s rpg_tw_home matches 15 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_15
execute if score @s rpg_tw_home matches 16 run data modify storage rpg:events v.home set value "亚实基伦"
execute if score @s rpg_tw_home matches 16 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_16
execute if score @s rpg_tw_home matches 17 run data modify storage rpg:events v.home set value "但城"
execute if score @s rpg_tw_home matches 17 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_17
execute if score @s rpg_tw_home matches 18 run data modify storage rpg:events v.home set value "撒勒法"
execute if score @s rpg_tw_home matches 18 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_18
execute if score @s rpg_tw_home matches 19 run data modify storage rpg:events v.home set value "雅比"
execute if score @s rpg_tw_home matches 19 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_19
execute if score @s rpg_tw_home matches 20 run data modify storage rpg:events v.home set value "以马忤斯"
execute if score @s rpg_tw_home matches 20 store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_20
execute store result storage rpg:events v.bn int 1 run scoreboard players get @s rpg_xb_n
execute store result storage rpg:events v.tn int 1 run scoreboard players get @s rpg_xt_n
execute store result storage rpg:events v.pt int 1 run scoreboard players get @s rpg_x_pt
function rpg:events/jr/body with storage rpg:events v
