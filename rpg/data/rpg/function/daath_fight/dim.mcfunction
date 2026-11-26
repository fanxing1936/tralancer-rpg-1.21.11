# 维度里有人才跑（in rpg:daath）
execute as @e[type=minecraft:marker,tag=rpg.dt.c] at @s run function rpg:daath_fight/arena/tick
execute as @e[type=minecraft:vindicator,tag=rpg.dtb,distance=0..] at @s rotated ~ 0 run function rpg:daath_fight/unit/tick
execute as @e[tag=rpg.dt.fx,distance=0..] at @s run function rpg:daath_fight/fx/tick
execute as @e[type=minecraft:item_display,tag=rpg.dt.shot,distance=0..] at @s run function rpg:daath_fight/shot/tick
execute as @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=0..] at @s run function rpg:daath_fight/minion/tick
execute as @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=0..] at @s unless entity @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..12] run kill @s
