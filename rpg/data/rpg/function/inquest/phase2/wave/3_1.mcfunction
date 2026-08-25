execute if score @s rpg_ex_wave matches 12 run particle dust_color_transition{from_color:[0.57,0.57,0.61],to_color:[0.04,0.03,0.07],scale:2.2} ~ ~0.35 ~ 14 0.15 14 0.05 108 force
execute if score @s rpg_ex_wave matches 12 run particle ash ~ ~1.1 ~ 14 1.6 14 0.08 94 force
execute if score @s rpg_ex_wave matches 12 run particle soul ~ ~1.5 ~ 9 1.0 9 0.035 42 force
execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle sculk_charge_pop ~ ~1 ~ 0.42 0.65 0.42 0.05 14 force
execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 2 minecraft:magic
execute if score @s rpg_ex_wave matches 12 run playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 0.8 0.68
execute if score @s rpg_ex_wave matches 1 run particle flash{color:6974064} ~ ~1.2 ~ 0 0 0 0 1 force
execute if score @s rpg_ex_wave matches 1 run particle dust_color_transition{from_color:[0.57,0.57,0.61],to_color:[0.04,0.03,0.07],scale:3.0} ~ ~0.35 ~ 17 0.2 17 0.06 142 force
execute if score @s rpg_ex_wave matches 1 run particle ash ~ ~1.3 ~ 18 2.2 18 0.10 126 force
execute if score @s rpg_ex_wave matches 1 run particle reverse_portal ~ ~1.4 ~ 12 1.4 12 0.06 62 force
execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle sculk_charge_pop ~ ~1 ~ 0.68 0.9 0.68 0.07 20 force
execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 4 minecraft:magic
execute if score @s rpg_ex_wave matches 1 run playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..36] ~ ~ ~ 1.2 0.62
