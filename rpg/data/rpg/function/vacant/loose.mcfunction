# 附近没有第二具躯体可用。那东西只好赤裸地留在原地。
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.6 0.6 0.6 0.15 60
execute at @s run playsound minecraft:entity.warden.roar hostile @a[distance=..28] ~ ~ ~ 0.8 1.4
execute at @s run summon minecraft:vex ~ ~1 ~ {life_ticks:900,Tags:["rpg.vac.shard"],CustomName:[{"text":"无处可去者","color":"dark_purple"}],Health:16f,attributes:[{id:"max_health",base:16f},{id:"attack_damage",base:5f}]}
execute at @s run summon minecraft:vex ~ ~1 ~ {life_ticks:900,Tags:["rpg.vac.shard"],CustomName:[{"text":"无处可去者","color":"dark_purple"}],Health:16f,attributes:[{id:"max_health",base:16f},{id:"attack_damage",base:5f}]}
execute at @s run summon minecraft:vex ~ ~1 ~ {life_ticks:900,Tags:["rpg.vac.shard"],CustomName:[{"text":"无处可去者","color":"dark_purple"}],Health:16f,attributes:[{id:"max_health",base:16f},{id:"attack_damage",base:5f}]}
title @s times 10 50 20
title @s title ["",{"text":"无 处 可 去","italic":false,"color":"dark_purple","bold":true}]
