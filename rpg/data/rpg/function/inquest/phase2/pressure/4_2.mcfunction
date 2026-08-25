scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 42
particle flash{color:5925662} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.72,0.78,0.29],to_color:[0.14,0.17,0.03],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 82 force
particle dust_color_transition{from_color:[0.72,0.78,0.29],to_color:[0.14,0.17,0.03],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 116 force
particle infested ~ ~1.15 ~ 12 1.8 12 0.07 138 force
particle mycelium ~ ~1.55 ~ 8 1.2 8 0.045 58 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪域·别西卜] ","color":"#5A6B1E","italic":false,"bold":true},{"text":"万蝇蔽日 · 三重罪域爆发，退入法阵四格庇护圈。","color":"gray","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle infested ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle item_slime ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 7 minecraft:magic
playsound minecraft:entity.spider.ambient hostile @a[distance=..32] ~ ~ ~ 0.95 0.88
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:blindness 5 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:weakness 9 2 true
