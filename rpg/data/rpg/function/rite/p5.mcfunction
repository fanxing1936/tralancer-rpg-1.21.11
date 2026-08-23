# 一拍净化。图腾每燃尽一分，效力就弱一分 —— 净化量由调用处给。
particle end_rod ~ ~0.5 ~ 3.0 0.2 3.0 0.04 70
particle dust{color:[1.0,0.98,0.86],scale:2} ~ ~0.8 ~ 3.0 0.4 3.0 0.03 60
playsound minecraft:block.conduit.ambient player @a[distance=..20] ~ ~ ~ 1 1.3
execute as @a[distance=..6] run scoreboard players remove @s rpg_taint 4
execute as @a[distance=..6,scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
# 图腾随着燃尽一点点缩小
data merge entity @s {transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.40f,0.40f,0.40f],right_rotation:[0f,0f,0f,1f]}}
