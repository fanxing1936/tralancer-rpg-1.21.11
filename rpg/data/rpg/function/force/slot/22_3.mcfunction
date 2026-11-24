execute unless score @s rpg_k22 matches 1.. run return run function rpg:force/fail/say {m:"先学会「恐惧」"}
execute if score @s rpg_fs_m1 matches 22 run scoreboard players set @s rpg_fs_m1 0
execute if score @s rpg_fs_m2 matches 22 run scoreboard players set @s rpg_fs_m2 0
scoreboard players set @s rpg_fs_m3 22
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
