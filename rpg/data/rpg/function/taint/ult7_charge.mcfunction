particle dust{color:[0.89,0.73,0.23],scale:1.7} ~ ~1 ~ 0.55 0.75 0.55 0.02 3 normal
particle wax_on ~ ~1 ~ 0.6 0.7 0.6 0.04 4 normal
execute if score @s rpg_dm_ult matches 20 run particle flash{color:14858555} ~ ~1 ~ 0 0 0 0 1 normal
execute if score @s rpg_dm_ult matches 20 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.65
execute if score @s rpg_dm_ult matches 10 run particle dust{color:[0.89,0.73,0.23],scale:3.2} ~ ~1 ~ 2.2 1.2 2.2 0.08 48 normal
execute if score @s rpg_dm_ult matches 10 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 1.1 1.1
