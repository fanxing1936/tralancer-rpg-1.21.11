scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 22
particle flash{color:1789810} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.24,0.66,0.91],to_color:[0.02,0.09,0.18],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 82 force
particle dust_color_transition{from_color:[0.24,0.66,0.91],to_color:[0.02,0.09,0.18],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 116 force
particle bubble ~ ~1.15 ~ 12 1.8 12 0.07 138 force
particle bubble_column_up ~ ~1.55 ~ 8 1.2 8 0.045 58 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪域·利维坦] ","color":"#1B4F72","italic":false,"bold":true},{"text":"逆潮回卷 · 三重罪域爆发，退入法阵四格庇护圈。","color":"gray","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle bubble ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle bubble_pop ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 7 minecraft:magic
playsound minecraft:entity.guardian.attack hostile @a[distance=..32] ~ ~ ~ 0.95 0.88
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:nausea 7 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:weakness 8 1 true
execute as @a[distance=8..20,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^2
