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
function rpg:events/jr/body with storage rpg:events v
