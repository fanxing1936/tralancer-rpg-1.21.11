execute if score @s rpg_ex_wave matches 12 run particle dust_color_transition{from_color:[0.72,0.78,0.29],to_color:[0.14,0.17,0.03],scale:2.2} ~ ~0.35 ~ 14 0.15 14 0.05 108 force
execute if score @s rpg_ex_wave matches 12 run particle item{item:{id:"minecraft:poisonous_potato"}} ~ ~1.1 ~ 14 1.6 14 0.08 94 force
execute if score @s rpg_ex_wave matches 12 run particle mycelium ~ ~1.5 ~ 9 1.0 9 0.035 42 force
execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle infested ~ ~1 ~ 0.42 0.65 0.42 0.05 14 force
execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 2 minecraft:magic
execute if score @s rpg_ex_wave matches 12 run playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 0.8 0.68
execute if score @s rpg_ex_wave matches 1 run particle flash{color:5925662} ~ ~1.2 ~ 0 0 0 0 1 force
execute if score @s rpg_ex_wave matches 1 run particle dust_color_transition{from_color:[0.72,0.78,0.29],to_color:[0.14,0.17,0.03],scale:3.0} ~ ~0.35 ~ 17 0.2 17 0.06 142 force
execute if score @s rpg_ex_wave matches 1 run particle item{item:{id:"minecraft:poisonous_potato"}} ~ ~1.3 ~ 18 2.2 18 0.10 126 force
execute if score @s rpg_ex_wave matches 1 run particle ash ~ ~1.4 ~ 12 1.4 12 0.06 62 force
execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle infested ~ ~1 ~ 0.68 0.9 0.68 0.07 20 force
execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:magic
execute if score @s rpg_ex_wave matches 1 run playsound minecraft:entity.spider.ambient hostile @a[distance=..36] ~ ~ ~ 1.2 0.62
