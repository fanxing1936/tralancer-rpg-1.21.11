execute if score @s rpg_ex_wave matches 12 run particle dust_color_transition{from_color:[0.9,0.64,0.24],to_color:[0.72,0.58,0.04],scale:2.2} ~ ~0.35 ~ 14 0.15 14 0.05 64 force
execute if score @s rpg_ex_wave matches 12 run particle totem_of_undying ~ ~1.1 ~ 14 1.6 14 0.08 56 force
execute if score @s rpg_ex_wave matches 12 run particle end_rod ~ ~1.5 ~ 9 1.0 9 0.035 28 force
execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle firework ~ ~1 ~ 0.42 0.65 0.42 0.05 10 normal
execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 2 minecraft:magic
execute if score @s rpg_ex_wave matches 12 run playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 0.8 0.68
execute if score @s rpg_ex_wave matches 1 run particle flash{color:15114812} ~ ~1.2 ~ 0 0 0 0 1 force
execute if score @s rpg_ex_wave matches 1 run particle dust_color_transition{from_color:[0.9,0.64,0.24],to_color:[0.72,0.58,0.04],scale:3.0} ~ ~0.35 ~ 17 0.2 17 0.06 88 force
execute if score @s rpg_ex_wave matches 1 run particle totem_of_undying ~ ~1.3 ~ 18 2.2 18 0.10 80 force
execute if score @s rpg_ex_wave matches 1 run particle wax_on ~ ~1.4 ~ 12 1.4 12 0.06 40 force
execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle firework ~ ~1 ~ 0.68 0.9 0.68 0.07 14 normal
execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:magic
execute if score @s rpg_ex_wave matches 1 run playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..36] ~ ~ ~ 1.2 0.62
