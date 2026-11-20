execute if score @s rpg_sl_t matches 7 run execute at @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] run function rpg:saul_boss/web/place
execute if score @s rpg_sl_t matches 7 run playsound minecraft:entity.spider.ambient hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute if score @s rpg_sl_t matches 19.. run function rpg:saul_boss/sk/end
