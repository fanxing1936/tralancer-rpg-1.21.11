scoreboard players remove @s rpg_fg_ec 1
execute if score @s rpg_fg_ec matches 1.. run return 0
scoreboard players operation #t rpg_fg = @s rpg_fg_eo
execute as @a if score @s rpg_fg_id = #t rpg_fg run tag @s add rpg.fg.eo
execute store result storage rpg:forge dmg.n int 1 run scoreboard players get @s rpg_fg_ea
execute if entity @a[tag=rpg.fg.eo] run function rpg:forge/rune/echo_hit with storage rpg:forge dmg
tag @a[tag=rpg.fg.eo] remove rpg.fg.eo
