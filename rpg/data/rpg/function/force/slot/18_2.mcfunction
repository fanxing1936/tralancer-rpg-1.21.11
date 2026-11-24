execute unless score @s rpg_k18 matches 1.. run return run function rpg:force/fail/say {m:"先学会「汲取」"}
execute if score @s rpg_fs_m1 matches 18 run scoreboard players set @s rpg_fs_m1 0
execute if score @s rpg_fs_m3 matches 18 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m2 18
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
