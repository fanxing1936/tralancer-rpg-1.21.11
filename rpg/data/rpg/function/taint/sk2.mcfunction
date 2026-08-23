# 利维坦［沉锚］—— 锚落处涌起漩涡，把人拖向锚心。
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle bubble_column_up ~ ~0.5 ~ 2 0.5 2 0.4 80
particle dust{color:[0.11,0.31,0.45],scale:3} ~ ~1 ~ 2 1 2 0.05 60
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^1.2
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
