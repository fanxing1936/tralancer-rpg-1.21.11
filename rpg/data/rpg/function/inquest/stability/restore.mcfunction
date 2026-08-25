scoreboard players add @s rpg_ex_stab 15
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_path=1,rpg_ex_lvl=2..}] run scoreboard players add @s rpg_ex_stab 5
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[distance=..10,gamemode=!spectator] rpg_ex_xp 3
function rpg:inquest/stability/show
