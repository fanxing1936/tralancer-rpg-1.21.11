execute unless score @s rpg_lt_divine matches 2 run return run function rpg:divine/authority/no_covenant
execute if score @s rpg_lt_judge matches 1.. run return run function rpg:divine/judgment/already_armed
execute unless score @s rpg_lt_auth matches 25.. run return run function rpg:divine/authority/insufficient
scoreboard players remove @s rpg_lt_auth 25
scoreboard players set @s rpg_lt_auth_t 0
scoreboard players set @s rpg_lt_judge 600
particle dust_color_transition{from_color:[0.38,0.85,0.91],to_color:[1.0,0.95,0.66],scale:1.5} ~ ~1 ~ 0.45 0.75 0.45 0.04 36 force
particle minecraft:end_rod ~ ~1 ~ 0.35 0.65 0.35 0.03 24 force
playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 1.55
function rpg:hud/m63
