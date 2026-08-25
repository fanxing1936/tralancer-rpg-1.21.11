scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 33
particle flash{color:6974064} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.57,0.57,0.61],to_color:[0.04,0.03,0.07],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 82 force
particle dust_color_transition{from_color:[0.57,0.57,0.61],to_color:[0.04,0.03,0.07],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 116 force
particle large_smoke ~ ~1.15 ~ 12 1.8 12 0.07 138 force
particle soul ~ ~1.55 ~ 8 1.2 8 0.045 58 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪域·亚巴顿] ","color":"#6A6A70","italic":false,"bold":true},{"text":"深渊张口 · 三重罪域爆发，退入法阵四格庇护圈。","color":"gray","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle large_smoke ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle sculk_charge_pop ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 11 minecraft:magic
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 0.95 0.96
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:darkness 9 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:levitation 3 0 true
execute as @a[distance=8..24,gamemode=!spectator,gamemode=!creative] run damage @s 4 minecraft:magic
