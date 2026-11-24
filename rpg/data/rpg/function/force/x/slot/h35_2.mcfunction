execute unless score @s rpg_k35 matches 1.. run return run function rpg:force/fail/say {m:"还没习得「注视」"}
execute unless score @s rpg_force matches 1 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有圣力"}
execute if score @s rpg_fs_h1 matches 35 run scoreboard players set @s rpg_fs_h1 0
execute if score @s rpg_fs_h3 matches 35 run scoreboard players set @s rpg_fs_h3 0
scoreboard players set @s rpg_fs_h2 35
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
