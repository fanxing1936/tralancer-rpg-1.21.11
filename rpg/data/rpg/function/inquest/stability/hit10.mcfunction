scoreboard players remove @s rpg_ex_stab 10
execute if entity @s[tag=rpg.layout.guard] run scoreboard players add @s rpg_ex_stab 4
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_path=2,rpg_ex_lvl=2..}] run scoreboard players add @s rpg_ex_stab 4
execute if score @s rpg_ex_stab matches ..0 run scoreboard players set @s rpg_ex_stab 0
function rpg:inquest/stability/show
