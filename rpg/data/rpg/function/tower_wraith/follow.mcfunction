# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:tower_wraith/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:tower_wraith/hurt
execute if predicate rpg:tower_wraith/ambient run playsound rpg:tower_wraith.idle hostile @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_tw matches 1.. run scoreboard players remove @s rpg_tw 1
execute if score @s rpg_tw matches ..0 unless score @s rpg_tw_anim matches 2..3 if entity @s[type=minecraft:pillager] if entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run function rpg:tower_wraith/strike
execute if score @s rpg_tw matches ..0 unless score @s rpg_tw_anim matches 2..3 if entity @s[type=minecraft:evoker] if entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run function rpg:tower_wraith/strike
execute if score @s rpg_tw matches ..0 unless score @s rpg_tw_anim matches 2..3 unless entity @s[type=minecraft:pillager] unless entity @s[type=minecraft:evoker] if entity @a[distance=..3.2,gamemode=!spectator,gamemode=!creative,limit=1] run function rpg:tower_wraith/strike
