execute if score #c4 rpg_pl matches 1..2 unless entity @a[distance=..32,gamemode=!spectator] run scoreboard players add #f4 rpg_pl 1
execute if entity @a[distance=..32,gamemode=!spectator] run scoreboard players set #f4 rpg_pl 0
execute if score #f4 rpg_pl matches 60.. run return run function rpg:pl/court/4/fail
execute if score #c4 rpg_pl matches 1 if block ~ ~2 ~ minecraft:trial_spawner[trial_spawner_state=cooldown] unless entity @e[tag=rpg.pl.g,distance=..28] run return run function rpg:pl/court/4/clear
execute if score #c4 rpg_pl matches 2.. run scoreboard players add #r4 rpg_pl 1
execute if score #c4 rpg_pl matches 2 if score #r4 rpg_pl matches 8.. run return run function rpg:pl/court/4/next
execute if score #c4 rpg_pl matches 3 if score #r4 rpg_pl matches 300.. run scoreboard players set #c4 rpg_pl 0
