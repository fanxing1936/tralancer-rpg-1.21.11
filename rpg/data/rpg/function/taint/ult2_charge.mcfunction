particle dust{color:[0.24,0.66,0.91],scale:1.7} ~ ~1 ~ 0.55 0.75 0.55 0.02 3 normal
particle bubble_column_up ~ ~0.4 ~ 0.6 0.2 0.6 0.16 5 normal
execute if score @s rpg_dm_ult matches 20 run particle flash{color:4041192} ~ ~1 ~ 0 0 0 0 1 normal
execute if score @s rpg_dm_ult matches 20 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.65
execute if score @s rpg_dm_ult matches 10 run particle dust{color:[0.24,0.66,0.91],scale:3.2} ~ ~1 ~ 2.2 1.2 2.2 0.08 48 normal
execute if score @s rpg_dm_ult matches 10 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 1.1 1.1
