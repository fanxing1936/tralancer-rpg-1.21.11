# 深渊之口 —— 地底下那张嘴张开了。
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 1 0.8
particle sonic_boom ~ ~1 ~ 0 0 0 0 3
particle sculk_charge_pop ~ ~0.2 ~ 4 0.3 4 0.2 120
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3c_maw
