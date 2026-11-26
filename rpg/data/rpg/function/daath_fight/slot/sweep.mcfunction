execute as @e[type=minecraft:vindicator,tag=rpg.dtb,distance=..120] run function rpg:daath_fight/unit/vanish
execute as @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..120] run function rpg:daath_fight/unit/vanish
kill @e[tag=rpg.dt.fx,distance=..120]
kill @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60]
kill @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60]
kill @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..60]
kill @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..60]
kill @e[type=minecraft:item_display,tag=rpg.dt.tree,distance=..60]
