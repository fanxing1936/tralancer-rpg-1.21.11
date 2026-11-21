scoreboard players add @a[tag=rpg.fg.atk,limit=1] rpg_fg_hit 1
execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_hit=4..}] run function rpg:forge/rune/echo_arm
