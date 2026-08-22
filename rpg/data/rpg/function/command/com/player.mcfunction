execute as @a[tag=rpg.h.skull_tag1] at @s if entity @s[tag=!rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player
execute as @a[tag=rpg.h.player_tag1] at @s run item modify entity @s weapon.mainhand rpg:command/player_value
