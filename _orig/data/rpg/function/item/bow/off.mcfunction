execute as @e[type=minecraft:arrow] on origin if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{dark_tag:1b}}}}] at @s run tag @e[type=arrow,distance=0..2] add dark
execute as @e[tag=dark] at @s run particle dust_color_transition{from_color:[0.19,0.05,0.33],to_color:[0.0,0.0,0.0],scale:1} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 1 10
execute as @e[tag=dark] at @s if entity @e[distance=0..1] unless entity @e[distance=0..1,nbt={SelectedItem:{components:{"minecraft:custom_data":{dark_tag:1b}}}}] at @s run tag @e[distance=0..1,type=!arrow] add darkness
execute as @e[tag=darkness] at @s if entity @e[distance=0..2] unless entity @e[distance=0..2,nbt={SelectedItem:{components:{"minecraft:custom_data":{dark_tag:1b}}}}] at @s run tag @e[distance=0..2,type=!arrow] add darkness
execute as @e[tag=darkness] at @s run particle dust_color_transition{from_color:[0.19,0.05,0.33],to_color:[0.0,0.0,0.0],scale:1} ~0.5 ~ ~0.5 -1 -1 -1 1 20
execute as @e[tag=darkness] at @s run effect give @s wither 1 1 true
execute as @e[tag=darkness] at @s run scoreboard players add @s dark 1
execute as @e[tag=darkness,scores={dark=200..}] at @s run tag @s remove darkness
execute as @e[scores={dark=200..}] at @s run scoreboard players reset @s dark 



execute as @e[nbt={SelectedItem:{components:{"minecraft:custom_data":{projectiles_tag:1b}}}}] at @s run item modify entity @s weapon.mainhand rpg:item/bow/projectiles
