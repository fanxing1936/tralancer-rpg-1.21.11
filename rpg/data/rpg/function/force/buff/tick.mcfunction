# 火焰之剑 / 血刃（as/at 玩家，每刻）
execute if score @s rpg_fo_buf <= #now rpg_fo run return run scoreboard players set @s rpg_fo_buf 0
execute if score @s rpg_fo_bk matches 4 run particle minecraft:flame ^-0.35 ^1.1 ^0.45 0.05 0.08 0.05 0.01 1
execute if score @s rpg_fo_bk matches 14 run particle minecraft:dust{color:[0.65,0.05,0.12],scale:0.9} ^-0.35 ^1.1 ^0.45 0.06 0.08 0.06 0 1
execute unless score @s rpg_fo_dd matches 1.. run return 0
scoreboard players set @s rpg_fo_dd 0
scoreboard players operation #lv rpg_fo = @s rpg_fo_blv
tag @s add rpg.fo.me
execute if score @s rpg_fo_bk matches 4 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=rpg.hurt,distance=..6,limit=1,sort=nearest] at @s run function rpg:force/sk/4/proc
execute if score @s rpg_fo_bk matches 14 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=rpg.hurt,distance=..6,limit=1,sort=nearest] at @s run function rpg:force/sk/14/proc
tag @s remove rpg.fo.me
