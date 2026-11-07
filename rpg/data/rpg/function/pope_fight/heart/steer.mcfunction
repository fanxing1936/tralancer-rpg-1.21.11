execute rotated ~ 0 positioned ^1000 ^ ^ if entity @a[tag=rpg.pf.tgt,limit=1,distance=..999.5] at @s run return run function rpg:pope_fight/heart/turn_left
execute rotated ~ 0 positioned ^-1000 ^ ^ if entity @a[tag=rpg.pf.tgt,limit=1,distance=..999.5] at @s run return run function rpg:pope_fight/heart/turn_right
execute rotated ~ 0 positioned ^ ^ ^-1000 if entity @a[tag=rpg.pf.tgt,limit=1,distance=..1000] at @s run function rpg:pope_fight/heart/turn_right
