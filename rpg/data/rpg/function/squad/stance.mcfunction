# 跟随 ⇄ 驻守。
#
# 注意中间那个 9：直接写"0 改 1、1 改 0"两行，第一行改完第二行立刻看到 1
# 又给改回 0 —— 翻不过来。先把 1 挪到一个两条判定都碰不到的值上。
execute if entity @s[scores={rpg_sq_stance=1}] run scoreboard players set @s rpg_sq_stance 9
execute if entity @s[scores={rpg_sq_stance=0}] run scoreboard players set @s rpg_sq_stance 1
execute if entity @s[scores={rpg_sq_stance=9}] run scoreboard players set @s rpg_sq_stance 0

execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players operation @s rpg_sq_mode = #sq_stance rpg_squad
execute if entity @s[scores={rpg_sq_stance=0}] run function rpg:squad/say_follow
execute if entity @s[scores={rpg_sq_stance=1}] run function rpg:squad/say_hold
