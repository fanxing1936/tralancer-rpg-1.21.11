execute as @e[type=minecraft:arrow] on origin if entity @s[tag=rpg.h.burn_tag1] at @s run tag @e[type=arrow,distance=0..2] add burn
execute as @e[tag=burn] at @s run particle flame ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10
execute as @e[tag=burn] at @s if entity @e[distance=0.1..2] unless entity @a[tag=rpg.h.burn_tag1,distance=..2] run summon minecraft:spectral_arrow ~ ~10 ~ {Tags:["burn_tag"]}
execute as @e[tag=burn_tag] at @s run particle flame ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10 force
execute if entity @e[tag=burn] run function rpg:item/bow/legend/burn/burn/g0
execute if entity @e[tag=burn_tag] run function rpg:item/bow/legend/burn/burn/g1




