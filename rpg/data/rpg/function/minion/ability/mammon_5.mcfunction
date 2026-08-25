# 马可西亚斯 · 处刑者（玛门）
scoreboard players set @s rpg_mn_cd 75
particle dust_color_transition{from_color:[1.0,0.79,0.20],to_color:[0.28,0.17,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle wax_on ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
tag @s add rpg.demon.minion.caster
execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s 6 minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..8,limit=1]
effect give @a[distance=..4,gamemode=!spectator,gamemode=!creative] minecraft:weakness 3 0 true
tag @s remove rpg.demon.minion.caster
particle sweep_attack ~ ~1 ~ 0.9 0.5 0.9 0.04 10
