tag @s remove rpg.dt.seek
execute as @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60] at @s run tp @s @a[tag=rpg.dt.me,limit=1]
execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/ten/fx
tag @a[tag=rpg.dt.me,limit=1] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 16
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
playsound minecraft:entity.player.attack.strong hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
