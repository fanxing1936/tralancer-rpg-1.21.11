execute if entity @s[tag=!rpg.advent,tag=!rpg.pf.boss,tag=!rpg.pf.heart,tag=!rpg.exorcism.bound] facing entity @a[tag=rpg.pact.cast,limit=1] feet run tp @s ^ ^ ^3
effect give @s minecraft:slowness 5 3 true
effect give @s minecraft:weakness 8 2 true
damage @s 16 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
