execute unless score @s rpg_fg_en matches 100.. run return run function rpg:forge/stone/not_ready
scoreboard players set @s rpg_fg_en 0
execute if entity @s[tag=rpg.fg.st.rift] run function rpg:forge/stone/rift
execute if entity @s[tag=rpg.fg.st.frost] run function rpg:forge/stone/frost
execute if entity @s[tag=rpg.fg.st.shadow] run function rpg:forge/stone/shadow
execute if entity @s[tag=rpg.fg.st.blood] run function rpg:forge/stone/blood
execute if entity @s[tag=rpg.fg.st.gale] run function rpg:forge/stone/gale
execute if entity @s[tag=rpg.fg.st.volley] run function rpg:forge/stone/volley
execute if entity @s[tag=rpg.fg.st.banner] run function rpg:forge/stone/banner
