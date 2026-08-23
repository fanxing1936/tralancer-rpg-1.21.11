execute if entity @s[tag=rpg.taint.full] run return run function rpg:hud/tfall

# 先把魔化换算成格数，再按档分流 —— 每档的颜色与措辞不同。
scoreboard players operation @s rpg_hud_p = @s rpg_taint
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #taint_max rpg_hud

execute if entity @s[scores={rpg_taint=1..30}] run function rpg:hud/t1
execute if entity @s[scores={rpg_taint=31..60}] run function rpg:hud/t2
execute if entity @s[scores={rpg_taint=61..90}] run function rpg:hud/t3
execute if entity @s[scores={rpg_taint=91..100}] run function rpg:hud/t4
