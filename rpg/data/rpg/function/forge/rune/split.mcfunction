data modify storage rpg:forge owner set from entity @a[tag=rpg.fg.atk,limit=1] UUID
execute as @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,distance=1..8,tag=!rpg.fg.v,limit=2,sort=nearest,tag=!rpg.ally] run function rpg:forge/rune/split_one
scoreboard players set @a[tag=rpg.fg.atk] rpg_fg_crit 0
