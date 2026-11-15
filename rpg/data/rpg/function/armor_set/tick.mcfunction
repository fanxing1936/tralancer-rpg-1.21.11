# 套装检测的秒表：每 20 刻对全部玩家确认一次。
scoreboard players add #as rpg_as_clock 1
execute if score #as rpg_as_clock matches 20.. run function rpg:armor_set/second
