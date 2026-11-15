# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:mammon_servant/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:mammon_servant/hurt
execute if predicate rpg:mammon_servant/ambient run playsound rpg:mammon_servant.idle hostile @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_mms matches 1.. run scoreboard players remove @s rpg_mms 1
execute if score @s rpg_mms matches ..0 unless score @s rpg_mms_anim matches 2..3 if entity @s[type=minecraft:pillager] if entity @e[tag=rpg.unit.f,distance=..12,limit=1] run function rpg:mammon_servant/strike
execute if score @s rpg_mms matches ..0 unless score @s rpg_mms_anim matches 2..3 if entity @s[type=minecraft:evoker] if entity @e[tag=rpg.unit.f,distance=..12,limit=1] run function rpg:mammon_servant/strike
execute if score @s rpg_mms matches ..0 unless score @s rpg_mms_anim matches 2..3 unless entity @s[type=minecraft:pillager] unless entity @s[type=minecraft:evoker] if entity @e[tag=rpg.unit.f,distance=..3.2,limit=1] run function rpg:mammon_servant/strike
