scoreboard players set @s rpg_lub_k 0
scoreboard players add @s rpg_lub_j 1
execute if score @s rpg_lub_j matches 2.. run scoreboard players set @s rpg_lub_j 0
execute store result score #n rpg_lub if entity @e[tag=rpg.lub.unit]
execute if entity @s[tag=rpg.lu.phase2] if score @s rpg_lub_j matches 0 run return run function rpg:lucifer_boss/fs/thorn/start
execute if entity @s[tag=rpg.lu.phase2] run return run function rpg:lucifer_boss/fs/sword/start
execute if score @s rpg_lub_j matches 0 if score #n rpg_lub matches ..3 run return run function rpg:lucifer_boss/fs/brood/start
function rpg:lucifer_boss/fs/star/start
