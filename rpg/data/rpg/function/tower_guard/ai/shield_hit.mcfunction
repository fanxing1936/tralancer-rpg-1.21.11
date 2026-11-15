# 盾吃一下；从背后打算三下。
scoreboard players remove @s rpg_tg_sh 1
execute positioned ^ ^ ^-2 if entity @e[tag=rpg.unit.f,distance=..2.5] run scoreboard players remove @s rpg_tg_sh 2
execute if score @s rpg_tg_sh matches ..0 run function rpg:tower_guard/ai/shield_break
