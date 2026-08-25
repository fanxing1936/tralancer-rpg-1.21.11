# 格拉夏·拉波拉斯 · 处刑者（萨麦尔）
scoreboard players set @s rpg_mn_cd 75
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle soul_fire_flame ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
tag @s add rpg.demon.minion.caster
execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s 7 minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..8,limit=1]
effect give @a[distance=..4,gamemode=!spectator,gamemode=!creative] minecraft:glowing 3 0 true
tag @s remove rpg.demon.minion.caster
particle sweep_attack ~ ~1 ~ 0.9 0.5 0.9 0.04 10
