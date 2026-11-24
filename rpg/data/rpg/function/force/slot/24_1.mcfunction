execute unless score @s rpg_k24 matches 1.. run return run function rpg:force/fail/say {m:"先学会「借柱」"}
execute if score @s rpg_fs_m2 matches 24 run scoreboard players set @s rpg_fs_m2 0
execute if score @s rpg_fs_m3 matches 24 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m1 24
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
