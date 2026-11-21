scoreboard players remove @s rpg_fg_t 1
execute if entity @s[tag=rpg.fg.gale] run function rpg:forge/stone/gale_tick
execute if entity @s[tag=rpg.fg.volley] run function rpg:forge/stone/volley_tick
execute if entity @s[tag=rpg.fg.banner] run function rpg:forge/stone/banner_tick
execute if score @s rpg_fg_t matches ..0 if entity @s[tag=rpg.fg.banner] run kill @e[type=minecraft:item_display,tag=rpg.fg.bdisp,distance=..2,limit=1,sort=nearest]
execute if score @s rpg_fg_t matches ..0 run kill @s
