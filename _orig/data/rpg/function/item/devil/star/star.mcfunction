advancement revoke @s only rpg:devil/star
execute as @e[nbt={Tags:["devil"]},distance=..7] at @s run particle ominous_spawning ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 3 500 force
execute as @e[nbt={Tags:["devil"]},distance=..7] at @s run effect give @s minecraft:glowing 5 1 true
execute as @e[nbt={Tags:["devil"]},distance=..7] at @s run effect give @s minecraft:slowness 5 255 true
execute as @e[nbt={Tags:["devil2"]},distance=..7] at @s run particle ominous_spawning ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 3 500 force
execute as @e[nbt={Tags:["devil2"]},distance=..7] at @s run effect give @s minecraft:glowing 5 1 true
execute as @e[nbt={Tags:["devil2"]},distance=..7] at @s run effect give @s minecraft:slowness 5 255 true
item replace entity @s weapon.mainhand with air
