execute unless score @s rpg_l2_st matches 2 run return 0
execute if entity @s[tag=rpg.lu2f.morph] run return 0
scoreboard players add @s rpg_dm_cd 0
execute if score @s rpg_dm_cd matches 1.. run return run scoreboard players remove @s rpg_dm_cd 1
execute if entity @a[distance=..16,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_boss/cast
