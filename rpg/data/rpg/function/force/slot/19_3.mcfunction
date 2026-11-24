execute unless score @s rpg_k19 matches 1.. run return run function rpg:force/fail/say {m:"先学会「献祭」"}
execute if score @s rpg_fs_m1 matches 19 run scoreboard players set @s rpg_fs_m1 0
execute if score @s rpg_fs_m2 matches 19 run scoreboard players set @s rpg_fs_m2 0
scoreboard players set @s rpg_fs_m3 19
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
