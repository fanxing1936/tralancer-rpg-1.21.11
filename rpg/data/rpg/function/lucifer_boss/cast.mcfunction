scoreboard players set @s rpg_dm_cd 70
scoreboard players set #ult rpg_lub 0
execute if score @s rpg_lub matches 1 if score @s rpg_lub_h matches ..626 unless entity @s[tag=rpg.lub.u1] run scoreboard players set #ult rpg_lub 1
execute if score @s rpg_lub matches 1 if score @s rpg_lub_h matches ..376 unless entity @s[tag=rpg.lub.u2] run scoreboard players set #ult rpg_lub 2
execute if score @s rpg_lub matches 1 if score #ult rpg_lub matches 0 if score @s rpg_lub_c matches 900.. run scoreboard players set #ult rpg_lub 9
execute if score @s rpg_lub matches 2 if score @s rpg_lub_h matches ..668 unless entity @s[tag=rpg.lub.u1] run scoreboard players set #ult rpg_lub 1
execute if score @s rpg_lub matches 2 if score @s rpg_lub_h matches ..334 unless entity @s[tag=rpg.lub.u2] run scoreboard players set #ult rpg_lub 2
execute if score @s rpg_lub matches 2 if score #ult rpg_lub matches 0 if score @s rpg_lub_c matches 1200.. run scoreboard players set #ult rpg_lub 9
execute if score #ult rpg_lub matches 1.. run return run function rpg:lucifer_boss/ult
tag @s add rpg.dm.cast
execute if entity @s[tag=rpg.lu.phase2] run function rpg:lucifer_fight/cast
execute unless entity @s[tag=rpg.lu.phase2] run function rpg:lucifer_fight/p1/cast
tag @s remove rpg.dm.cast
