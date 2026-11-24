execute if score #c2 rpg_pl matches 1..2 unless entity @a[distance=..32,gamemode=!spectator] run scoreboard players add #f2 rpg_pl 1
execute if entity @a[distance=..32,gamemode=!spectator] run scoreboard players set #f2 rpg_pl 0
execute if score #f2 rpg_pl matches 60.. run return run function rpg:pl/court/2/fail
execute if score #c2 rpg_pl matches 1 if block ~ ~1 ~ minecraft:trial_spawner[trial_spawner_state=cooldown] unless entity @e[tag=rpg.pl.g,distance=..28] run return run function rpg:pl/court/2/clear
execute if score #c2 rpg_pl matches 2.. run scoreboard players add #r2 rpg_pl 1
execute if score #c2 rpg_pl matches 2 if score #r2 rpg_pl matches 8.. run return run function rpg:pl/court/2/next
execute if score #c2 rpg_pl matches 3 if score #r2 rpg_pl matches 300.. run scoreboard players set #c2 rpg_pl 0
