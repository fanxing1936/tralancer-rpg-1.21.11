# 一轮切割。獠牙**长在每个目标自己的脚下**，而不是玩家身前的固定点 ——
# 原来那样常常整轮咬空，只剩显式伤害在生效。
# 獠牙沿用[切割链锯]的做法（放大、发光的 evoker_fangs），只是烧红了。
particle dust_color_transition{from_color:16553767,to_color:8005632,scale:2} ~ ~1 ~ 0.6 0.5 0.6 0.06 22
particle lava ~ ~0.8 ~ 0.5 0.4 0.5 0 6
playsound minecraft:item.axe.scrape player @a[distance=..18] ~ ~ ~ 1 1.6

execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:0,Tags:["rpg.saw.fang"],attributes:[{id:"scale",base:2.2f}]}
execute as @e[tag=rpg.saw.fang] run data modify entity @s Owner set from entity @p[tag=rpg.h.dawn_tag1] UUID
tag @e[tag=rpg.saw.fang] remove rpg.saw.fang

execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @p[tag=rpg.h.dawn_tag1]
# 熔岩锯齿咬过之后伤口一直在烧 —— 六轮之间的空档由灼烧填满，
# 目标因此是持续掉血，而不是每 10 刻才动一次。
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run data merge entity @s {Fire:120s}
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:glowing 3 0 true
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run particle trial_spawner_detection ~ ~1 ~ 0.4 0.5 0.4 0.1 10
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run playsound minecraft:entity.blaze.burn hostile @a[distance=..18] ~ ~ ~ 1 0.8
