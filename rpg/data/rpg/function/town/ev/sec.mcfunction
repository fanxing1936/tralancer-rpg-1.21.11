# 每秒：开场判断、进行中的副本、白天的风声
schedule function rpg:town/ev/sec 20t
execute store result score #tod rpg_te run time query daytime
execute if score #run rpg_te matches 1.. run return run function rpg:town/ev/step
execute if score #tod rpg_te matches 13000..13100 run function rpg:town/ev/night
scoreboard players add #rumor rpg_te 1
execute if score #rumor rpg_te matches 70.. if score #tod rpg_te matches 1000..12000 run function rpg:town/ev/rumors
