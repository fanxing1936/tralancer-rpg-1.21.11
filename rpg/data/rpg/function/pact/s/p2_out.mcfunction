execute if entity @s[tag=!rpg.advent,tag=!rpg.pf.boss,tag=!rpg.pf.heart,tag=!rpg.exorcism.bound] facing entity @a[tag=rpg.pact.cast,limit=1] feet run tp @s ^ ^ ^-2.4
damage @s 8 minecraft:drown by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
