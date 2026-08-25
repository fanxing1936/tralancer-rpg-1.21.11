scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 51
particle flash{color:8070172} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.89,0.30,0.30],to_color:[0.24,0.0,0.04],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 82 force
particle dust_color_transition{from_color:[0.89,0.30,0.30],to_color:[0.24,0.0,0.04],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 116 force
particle flame ~ ~1.15 ~ 12 1.8 12 0.07 138 force
particle soul_fire_flame ~ ~1.55 ~ 8 1.2 8 0.045 58 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪域·萨麦尔] ","color":"#7B241C","italic":false,"bold":true},{"text":"怒潮焚界 · 三重罪域爆发，退入法阵四格庇护圈。","color":"gray","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle flame ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle damage_indicator ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 9 minecraft:magic
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 0.95 0.80
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:weakness 8 1 true
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run data merge entity @s {Fire:80s}
