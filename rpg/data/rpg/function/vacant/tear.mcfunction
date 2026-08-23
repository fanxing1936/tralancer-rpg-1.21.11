# 壳裂开了。村民还站在那儿，但里面的东西跑了出来。
tag @s add rpg.vac.torn
effect give @s minecraft:speed 30 1 true
particle sculk_charge_pop ~ ~1.2 ~ 0.4 0.5 0.4 0.1 30
particle soul ~ ~1.2 ~ 0.3 0.4 0.3 0.05 20
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..24] ~ ~ ~ 0.7 1.8
summon minecraft:vex ~ ~1 ~ {life_ticks:600,Tags:["rpg.vac.shard"],CustomName:[{"text":"空壳碎片","color":"dark_purple"}],Health:12f,attributes:[{id:"max_health",base:12f},{id:"attack_damage",base:4f},{id:"scale",base:0.75f}]}
summon minecraft:vex ~ ~1 ~ {life_ticks:600,Tags:["rpg.vac.shard"],CustomName:[{"text":"空壳碎片","color":"dark_purple"}],Health:12f,attributes:[{id:"max_health",base:12f},{id:"attack_damage",base:4f},{id:"scale",base:0.75f}]}
title @a[distance=..12] actionbar ["",{"text":"壳裂开了","italic":true,"color":"dark_purple"}]
