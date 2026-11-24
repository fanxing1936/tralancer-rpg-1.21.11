# 每秒：满足条件的人计时加一，条件断了就清零
tag @a remove rpg.q.gate
tag @a remove rpg.q.sun
execute as @a[y=150,dy=400] if items entity @s weapon.mainhand *[minecraft:custom_data~{jachin_tag:1b}] if items entity @s weapon.offhand *[minecraft:custom_data~{boaz_tag:1b}] at @s run function rpg:quest/egg/gate_tick
execute as @a[scores={rpg_sef=10},x_rotation=-90..-60] if items entity @s weapon.mainhand *[minecraft:custom_data~{saber_tag:1b}] at @s run function rpg:quest/egg/meteor_tick
scoreboard players set @a[tag=!rpg.q.gate,scores={rpg_q_eg=1..}] rpg_q_eg 0
scoreboard players set @a[tag=!rpg.q.sun,scores={rpg_q_em=1..}] rpg_q_em 0
