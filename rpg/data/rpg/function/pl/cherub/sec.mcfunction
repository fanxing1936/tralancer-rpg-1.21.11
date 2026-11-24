scoreboard players add #ch rpg_pl 1
execute unless score #ch rpg_pl matches 2400.. run return 0
execute if entity @e[tag=rpg.pl.b.cherub] run return run scoreboard players set #ch rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 unless entity @a[distance=560..,gamemode=!spectator] run return 0
scoreboard players set #ch rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 as @r[distance=560..,gamemode=!spectator] at @s run function rpg:pl/cherub/spawn
