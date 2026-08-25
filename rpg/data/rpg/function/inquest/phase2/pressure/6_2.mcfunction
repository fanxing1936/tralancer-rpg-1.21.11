scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 62
particle flash{color:5975151} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 82 force
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 116 force
particle heart ~ ~1.15 ~ 12 1.8 12 0.07 138 force
particle reverse_portal ~ ~1.55 ~ 8 1.2 8 0.045 58 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪域·贝利尔] ","color":"#5B2C6F","italic":false,"bold":true},{"text":"顾盼夺心 · 三重罪域爆发，退入法阵四格庇护圈。","color":"gray","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle heart ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle enchanted_hit ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 9 minecraft:magic
playsound minecraft:entity.illusioner.prepare_mirror hostile @a[distance=..32] ~ ~ ~ 0.95 0.88
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:slowness 8 3 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:weakness 9 2 true
execute as @a[distance=6..18,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^-1.5
