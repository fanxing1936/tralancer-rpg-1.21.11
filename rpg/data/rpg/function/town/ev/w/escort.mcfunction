# 她跟着最近的参与者走（每秒一格多），到营地就停
scoreboard players add #tt rpg_te 1
execute if score #tt rpg_te matches 20 run function rpg:town/ev/w/l_iq04
execute if score #tt rpg_te matches 40 run function rpg:town/ev/w/l_ew09
execute if score #tt rpg_te matches 70 run function rpg:town/ev/w/l_iq05
execute as @e[tag=rpg.te.witch] at @s run particle minecraft:dust{color:[0.6,0.4,0.8],scale:1} ~ ~1 ~ 0.2 0.5 0.2 0 4
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.at.camp] if score @s rpg_tw_id = #run rpg_te at @s if entity @e[tag=rpg.te.witch,distance=..10] run function rpg:town/ev/w/arrive
