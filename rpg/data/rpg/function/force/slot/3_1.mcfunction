execute unless score @s rpg_k03 matches 1.. run return run function rpg:force/fail/say {m:"先学会「炽天之怒」"}
execute if score @s rpg_fs_h2 matches 3 run scoreboard players set @s rpg_fs_h2 0
execute if score @s rpg_fs_h3 matches 3 run scoreboard players set @s rpg_fs_h3 0
scoreboard players set @s rpg_fs_h1 3
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
