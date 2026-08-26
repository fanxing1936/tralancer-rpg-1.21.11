tag @e[tag=rpg.ch1.puzzle.enemy] remove rpg.ch1.puzzle.enemy.current
execute as @e[tag=rpg.ch1.puzzle.enemy] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.puzzle.enemy.current
kill @e[tag=rpg.ch1.puzzle.enemy.current,distance=72.01..]
