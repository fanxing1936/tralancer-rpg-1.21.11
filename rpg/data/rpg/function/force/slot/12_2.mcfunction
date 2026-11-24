execute unless score @s rpg_k12 matches 1.. run return run function rpg:force/fail/say {m:"先学会「升天」"}
execute if score @s rpg_fs_h1 matches 12 run scoreboard players set @s rpg_fs_h1 0
execute if score @s rpg_fs_h3 matches 12 run scoreboard players set @s rpg_fs_h3 0
scoreboard players set @s rpg_fs_h2 12
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
