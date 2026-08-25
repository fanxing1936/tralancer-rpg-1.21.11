# 反转的节拍：图腾朝着受术者烧，一拍比一拍狠。
# 人必须站在圈里熬完 —— 走开或者倒下，仪式当场作废。
# return run：失败要连这支图腾余下的节拍一起掐掉，否则后面几条会对着
# 一个已经 kill 掉的 @s 继续跑。
scoreboard players operation #inv_id rpg_inv_id = @s rpg_inv_id
scoreboard players set #inv_alive rpg_inv_id 0
execute as @a[tag=rpg.inv.subject,distance=..7] if score @s rpg_inv_id = #inv_id rpg_inv_id run scoreboard players set #inv_alive rpg_inv_id 1
execute unless score #inv_alive rpg_inv_id matches 1 run return run function rpg:rite/inv_fail
scoreboard players operation #inv_now rpg_hud = @s rpg_totem
execute as @a[tag=rpg.inv.subject,distance=..7] if score @s rpg_inv_id = #inv_id rpg_inv_id run function rpg:rite/inv_hud
execute if entity @s[scores={rpg_totem=200}] run function rpg:rite/v1
execute if entity @s[scores={rpg_totem=160}] run function rpg:rite/v2
execute if entity @s[scores={rpg_totem=120}] run function rpg:rite/v3
execute if entity @s[scores={rpg_totem=80}] run function rpg:rite/v4
execute if entity @s[scores={rpg_totem=40}] run function rpg:rite/v5
particle soul_fire_flame ~ ~0.8 ~ 0.45 0.55 0.45 0.02 3
particle dust{color:[0.42,0.06,0.10],scale:2} ~ ~0.8 ~ 0.5 0.6 0.5 0.01 2
execute if entity @s[scores={rpg_totem=1..}] run scoreboard players remove @s rpg_totem 1
execute if entity @s[scores={rpg_totem=..0}] run function rpg:rite/inv_burst
