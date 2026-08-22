# rpg:entities/drowned/magic is a 3568-command particle circle.  Only draw it
# when a player is close enough for the particles to render at all.
execute as @e[tag=drowned_tag] at @s if entity @a[distance=..48] run function rpg:entities/drowned/magic
execute as @e[tag=drowned_tag] at @s run effect give @s instant_damage 10 5 true
