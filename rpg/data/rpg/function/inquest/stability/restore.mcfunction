scoreboard players add @s rpg_ex_stab 15
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[distance=..10,gamemode=!spectator] rpg_ex_dxp 3
function rpg:inquest/stability/show
