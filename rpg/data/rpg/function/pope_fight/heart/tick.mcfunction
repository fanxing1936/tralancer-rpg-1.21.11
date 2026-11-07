# 末影之心一刻（as、at 判定体）。
scoreboard players add #h rpg_pf 1
execute if score #h rpg_pf matches 5.. run function rpg:pope_fight/heart/read
execute unless score #stage rpg_pf matches 4 run return 0
execute if score #bl rpg_pf matches 1.. run function rpg:pope_fight/heart/blend_tick
execute if score #cd rpg_pf matches 1.. run scoreboard players remove #cd rpg_pf 1
execute if score #ultcd rpg_pf matches 1.. run scoreboard players remove #ultcd rpg_pf 1
execute if entity @e[type=minecraft:armor_stand,tag=rpg.pf.face,limit=1] as @e[type=minecraft:armor_stand,tag=rpg.pf.face] at @s run function rpg:pope_fight/heart/face_tick
execute if score #sk rpg_pf matches 1.. run return run function rpg:pope_fight/heart/skill
execute unless entity @a[tag=rpg.pf.tgt,limit=1] run return run function rpg:pope_fight/heart/stop
function rpg:pope_fight/heart/free
