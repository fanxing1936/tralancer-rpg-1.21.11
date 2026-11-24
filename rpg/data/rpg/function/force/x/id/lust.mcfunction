execute unless entity @a[tag=rpg.fo.me,limit=1,scores={rpg_sef=5..}] run effect give @s minecraft:weakness 1 0 true
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_sef=5..}] run effect give @s minecraft:weakness 2 0 true
particle minecraft:dust{color:[0.85,0.48,0.85],scale:0.8} ~ ~1.2 ~ 0.2 0.3 0.2 0 4
