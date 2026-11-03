scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 71
particle flash{color:12031243} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.9,0.64,0.24],to_color:[0.72,0.58,0.04],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 82 force
particle dust_color_transition{from_color:[0.9,0.64,0.24],to_color:[0.72,0.58,0.04],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 116 force
particle wax_on ~ ~1.15 ~ 12 1.8 12 0.07 138 force
particle end_rod ~ ~1.55 ~ 8 1.2 8 0.045 58 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪域・玛门] ","color":"#E6A23C","bold":true,"italic":false},{"text":"黄金牢城 · 三重罪域爆发，退入法阵四格庇护圈。","color":"gray","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle wax_on ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle firework ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:magic
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 0.95 0.80
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:slowness 10 4 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:mining_fatigue 10 2 true
