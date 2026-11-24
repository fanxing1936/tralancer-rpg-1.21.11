# 罪潮之夜里打倒首领（as 玩家）
execute unless score #tide rpg_ev matches 1 run return 0
scoreboard players add @s rpg_ev_tc 1
execute if score @s rpg_ev_tc matches 3 unless entity @s[tag=rpg.ev.yesod] run function rpg:events/e1/yesod
