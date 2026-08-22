execute as @e[type=minecraft:arrow] on origin if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{burn_tag:1b}}}}] at @s run tag @e[type=arrow,distance=0..2] add burn
execute as @e[tag=burn] at @s run particle flame ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10
execute as @e[tag=burn] at @s if entity @e[distance=0.1..2] unless entity @e[nbt={SelectedItem:{components:{"minecraft:custom_data":{burn_tag:1b}}}},distance=..2] run summon minecraft:spectral_arrow ~ ~10 ~ {Tags:["burn_tag"]}
execute as @e[nbt={Tags:["burn_tag"]}] at @s run particle flame ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10 force
execute as @e[tag=burn] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=burn] at @s unless block ~ ~ ~0.1 air run kill @s
execute as @e[nbt={Tags:["burn_tag"]}] at @s unless block ~ ~-0.1 ~ air run damage @e[limit=1,sort=nearest,distance=0.1..1] 5 minecraft:on_fire
execute as @e[nbt={Tags:["burn_tag"]}] at @s unless block ~ ~-0.1 ~ air run particle lava ~1 ~1 ~1 0 -2 -2 1 100 force
execute as @e[nbt={Tags:["burn_tag"]}] at @s unless block ~ ~-0.1 ~ air run kill @s




