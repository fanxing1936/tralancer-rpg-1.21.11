execute unless score @s rpg_k34 matches 1.. run return run function rpg:force/fail/say {m:"还没习得「千刀」"}
execute unless score @s rpg_force matches 2 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有魔力"}
execute if score @s rpg_fs_m1 matches 34 run scoreboard players set @s rpg_fs_m1 0
execute if score @s rpg_fs_m3 matches 34 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m2 34
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
