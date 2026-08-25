scoreboard players add @s rpg_ex_stab 2
execute if entity @s[tag=rpg.layout.haste] run scoreboard players add @s rpg_ex_stab 1
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
function rpg:inquest/stability/show
particle end_rod ~ ~0.7 ~ 0.25 0.15 0.25 0.02 4 normal
