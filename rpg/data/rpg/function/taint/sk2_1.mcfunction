# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/2_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m6
# 沉锚 —— 锚落处涌起漩涡，把人拖向锚心。
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle bubble_column_up ~ ~0.5 ~ 2 0.5 2 0.4 80
particle dust{color:[0.11,0.31,0.45],scale:3} ~ ~1 ~ 2 1 2 0.05 60
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^1.2
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:inquest/seal/ability/record_magic
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
