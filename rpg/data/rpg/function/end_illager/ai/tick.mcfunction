# 术士一刻（as/at 载体）。0 自由，1 放圣光弹，2 祝圣同伴。
execute unless score @s rpg_ei_st matches 0.. run function rpg:end_illager/ai/init
execute if score @s rpg_ei_st matches 1 run return run function rpg:end_illager/ai/cast
execute if score @s rpg_ei_st matches 2 run return run function rpg:end_illager/ai/heal
scoreboard players remove @s[scores={rpg_ei_cd=1..}] rpg_ei_cd 1
scoreboard players remove @s[scores={rpg_ei_bc=1..}] rpg_ei_bc 1
scoreboard players remove @s[scores={rpg_ei_hc=1..}] rpg_ei_hc 1
execute if score @s rpg_ei_bc matches 0 if entity @e[tag=rpg.unit.f,distance=..4] run return run function rpg:end_illager/ai/blink
execute if score @s rpg_ei_hc matches 0 if entity @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.ei,distance=..12] run return run function rpg:end_illager/ai/heal_start
execute if score @s rpg_ei_cd matches 0 if entity @e[tag=rpg.unit.f,distance=5..20] run function rpg:end_illager/ai/cast_start
execute if entity @s[tag=rpg.hurt] run function rpg:end_illager/anim/enter/hurt
