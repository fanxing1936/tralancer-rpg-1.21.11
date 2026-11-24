# as/at 掉在原地的爆裂标记
scoreboard players add @s rpg_el_t 1
execute if score @s rpg_el_t matches ..19 run return run particle minecraft:dust{color:[1.00,0.64,0.36],scale:1.2} ~ ~0.5 ~ 0.6 0.3 0.6 0 4
particle minecraft:explosion ~ ~0.5 ~ 1 0.5 1 0 6
playsound minecraft:entity.generic.explode hostile @a[distance=..24] ~ ~ ~ 1 1
execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:explosion
kill @s
