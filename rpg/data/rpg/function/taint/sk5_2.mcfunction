# 怒斩 —— 暴怒不讲章法，它只是冲上来。
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle crit ~ ~1 ~ 1 1 1 0.4 60
execute at @s facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run tp @s ^ ^ ^4
execute as @a[distance=..6,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5b_slash
