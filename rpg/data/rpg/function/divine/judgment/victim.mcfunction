tag @s add rpg.divine.judgment.target
execute on attacker if entity @s[type=minecraft:player,scores={rpg_lt_divine=2,rpg_lt_judge=1..}] at @s run function rpg:divine/judgment/cast
tag @s remove rpg.divine.judgment.target
