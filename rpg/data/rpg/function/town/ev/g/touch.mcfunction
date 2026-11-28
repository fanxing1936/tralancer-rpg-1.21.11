advancement revoke @s only rpg:town/trace
execute as @e[type=minecraft:interaction,tag=rpg.te.tr1,distance=..6] at @s run function rpg:town/ev/g/found {n:1}
execute as @e[type=minecraft:interaction,tag=rpg.te.tr2,distance=..6] at @s run function rpg:town/ev/g/found {n:2}
execute as @e[type=minecraft:interaction,tag=rpg.te.tr3,distance=..6] at @s run function rpg:town/ev/g/found {n:3}
execute as @e[type=minecraft:interaction,tag=rpg.te.circle,distance=..6] run function rpg:town/ev/g/totem
