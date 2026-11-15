# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:samael_servant/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:samael_servant/hurt
execute if predicate rpg:samael_servant/ambient run playsound rpg:samael_servant.idle hostile @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_sms matches 1.. run scoreboard players remove @s rpg_sms 1
execute if score @s rpg_sms matches ..0 unless score @s rpg_sms_anim matches 2..3 if entity @s[type=minecraft:pillager] if entity @e[tag=rpg.unit.f,distance=..12,limit=1] run function rpg:samael_servant/strike
execute if score @s rpg_sms matches ..0 unless score @s rpg_sms_anim matches 2..3 if entity @s[type=minecraft:evoker] if entity @e[tag=rpg.unit.f,distance=..12,limit=1] run function rpg:samael_servant/strike
execute if score @s rpg_sms matches ..0 unless score @s rpg_sms_anim matches 2..3 unless entity @s[type=minecraft:pillager] unless entity @s[type=minecraft:evoker] if entity @e[tag=rpg.unit.f,distance=..3.2,limit=1] run function rpg:samael_servant/strike
