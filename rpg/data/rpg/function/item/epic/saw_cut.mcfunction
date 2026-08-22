# 一轮切割：身前召出熔岩獠牙，锯齿咬过 3.5 格。
# 獠牙沿用[切割链锯]的做法（放大、发光的 evoker_fangs），只是烧红了。
execute anchored eyes positioned ^ ^ ^2 run summon minecraft:evoker_fangs ~ ~-1 ~ {Warmup:0,Tags:["rpg.saw.fang"],attributes:[{id:"scale",base:2.2f}]}
execute as @e[tag=rpg.saw.fang] run data modify entity @s Owner set from entity @p[tag=rpg.h.dawn_tag1] UUID
tag @e[tag=rpg.saw.fang] remove rpg.saw.fang
particle trial_spawner_detection ~ ~1.2 ~ 0.5 0.5 0.5 0.1 12
particle lava ~ ~0.8 ~ 0.5 0.4 0.5 0 8
particle dust_color_transition{from_color:16553767,to_color:8005632,scale:2} ~ ~1 ~ 0.6 0.5 0.6 0.06 26
playsound minecraft:entity.blaze.burn player @a[distance=..18] ~ ~ ~ 1 0.8
playsound minecraft:item.axe.scrape player @a[distance=..18] ~ ~ ~ 1 1.6
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @p[tag=rpg.h.dawn_tag1]
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:glowing 3 0 true
