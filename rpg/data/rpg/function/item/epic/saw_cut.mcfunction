# 施法者只在本次调用里挂这个标签 —— 同一刻只可能有一个玩家挂着，
# 所以下面的 limit=1 是精确的，而不是"离目标最近的持锯者"。
tag @s add rpg.saw.cast
# 一轮切割。獠牙**长在每个目标自己的脚下**，而不是玩家身前的固定点 ——
# 原来那样常常整轮咬空，只剩显式伤害在生效。
# 獠牙沿用[切割链锯]的做法（放大、发光的 evoker_fangs），只是烧红了。
particle dust_color_transition{from_color:16553767,to_color:8005632,scale:2} ~ ~1 ~ 0.6 0.5 0.6 0.06 22
particle lava ~ ~0.8 ~ 0.5 0.4 0.5 0 6
playsound minecraft:item.axe.scrape player @a[distance=..18] ~ ~ ~ 1 1.6

execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:0,Tags:["rpg.saw.fang"],attributes:[{id:"scale",base:2.2f}]}
execute as @e[type=minecraft:evoker_fangs,tag=rpg.saw.fang,distance=..6] run data modify entity @s Owner set from entity @a[tag=rpg.saw.cast,limit=1] UUID
tag @e[type=minecraft:evoker_fangs,tag=rpg.saw.fang,distance=..6] remove rpg.saw.fang

execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @a[tag=rpg.saw.cast,limit=1]
# 熔岩锯齿咬过之后伤口一直在烧 —— 六轮之间的空档由灼烧填满，
# 目标因此是持续掉血，而不是每 10 刻才动一次。
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run data merge entity @s {Fire:120s}
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:glowing 3 0 true
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run particle trial_spawner_detection ~ ~1 ~ 0.4 0.5 0.4 0.1 10
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run playsound minecraft:entity.blaze.burn hostile @a[distance=..18] ~ ~ ~ 1 0.8
tag @s remove rpg.saw.cast
