# 面容一刻（as、at 盔甲架）。光束由盔甲架带着走。
scoreboard players remove @s rpg_pf_l 1
execute if score @s rpg_pf_l matches 60 at @s positioned ^1.31 ^1.97 ^3.00 run function rpg:pope_fight/fx/face_beam
execute if score @s rpg_pf_l matches 18..50 if entity @s[tag=rpg.pf.chase] run function rpg:pope_fight/heart/face_chase
execute if score @s rpg_pf_l matches 18..50 if entity @s[tag=rpg.pf.cw] at @s run tp @s ~ ~ ~ ~1.2 0
execute if score @s rpg_pf_l matches 18..50 if entity @s[tag=rpg.pf.ccw] at @s run tp @s ~ ~ ~ ~-1.2 0
execute if score @s rpg_pf_l matches 14..60 at @s positioned ^1.31 ^1.97 ^3.00 as @e[type=minecraft:text_display,tag=rpg.pf.fbeam,distance=..3,limit=3] run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_pf_l matches 18..50 if score #h rpg_pf matches 0 at @s positioned ^1.31 ^1.97 ^3.00 run function rpg:pope_fight/heart/face_ray
execute if score @s rpg_pf_l matches ..0 run function rpg:arch_visage/internal/clear
