# 白天的风声：每 70 秒，有人在的镇上，镇民说一句
scoreboard players set #rumor rpg_te 0
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] at @s if entity @a[distance=..120,gamemode=!spectator] run function rpg:town/ev/rumor_at
