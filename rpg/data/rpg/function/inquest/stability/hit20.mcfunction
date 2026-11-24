scoreboard players remove @s rpg_ex_stab 20
execute if entity @s[tag=rpg.layout.guard] run scoreboard players add @s rpg_ex_stab 8
execute if score @s rpg_ex_stab matches ..0 run scoreboard players set @s rpg_ex_stab 0
function rpg:inquest/stability/show
