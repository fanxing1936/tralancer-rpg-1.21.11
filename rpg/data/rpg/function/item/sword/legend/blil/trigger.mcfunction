advancement revoke @s only rpg:item/blil
execute as @s at @s anchored eyes run particle enchant ~0.5 ~0.5 ~0.5 -1 -1 -1 1 50
execute as @s at @s anchored eyes run particle dust_color_transition{from_color:[0.4,0.0,0.6],scale:1.5,to_color:[0.0,0.0,0.0]} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.3 10
execute as @s at @s run xp add @s -1 points
execute as @s at @s anchored eyes run damage @s 1
execute as @s at @s run effect give @e[distance=0.1..7] slowness 2 255 true
execute as @s at @s at @e[distance=0.1..7] run particle dust_color_transition{from_color:[0.4,0.0,0.6],scale:1.5,to_color:[0.0,0.0,0.0]} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.3 3
execute as @e[distance=0.1..7] at @s run damage @s 3
