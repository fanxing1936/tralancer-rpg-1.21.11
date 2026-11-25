scoreboard players add #rf rpg_pl 1
execute unless score #rf rpg_pl matches 2.. run return 0
scoreboard players set #rf rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 as @a[distance=0..] at @s if predicate rpg:paradise/open_sky run function rpg:pl/rain/fx
