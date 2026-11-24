execute unless score @s rpg_k23 matches 1.. run return run function rpg:force/fail/say {m:"先学会「傀儡」"}
execute if score @s rpg_fs_m2 matches 23 run scoreboard players set @s rpg_fs_m2 0
execute if score @s rpg_fs_m3 matches 23 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m1 23
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
