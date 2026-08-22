execute as @e at @s on attacker if entity @s[scores={saber=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] store result score @s random run random value 1..10
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] wither 10 40 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":2,"Fuse":0}
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/flame
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @s resistance 5 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:1} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20


execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] minecraft:wither 20 40 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run particle minecraft:soul_fire_flame ~1 ~1.5 ~1 -2 -2 -2 0.5 100
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/particle
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @s resistance 1 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run playsound minecraft:item.mace.smash_ground_heavy 


execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @e[distance=0..1] minecraft:slowness 5 255 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run particle wax_off ~1 ~1.5 ~1 -2 -2 -2 1 100
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/spark
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @e[distance=0..1] minecraft:glowing 5 255 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @s resistance 1 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run playsound minecraft:item.mace.smash_ground_heavy 


execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] at @e[limit=1,sort=nearest] run summon lightning_bolt
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run particle minecraft:soul ~1 ~1.5 ~1 -2 -2 -2 0.5 100
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @s resistance 1 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/sweep


execute as @e at @s on attacker if entity @s[scores={saber=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run effect give @e[distance=0..2,limit=1,sort=nearest] minecraft:weakness 10 5 true
execute as @e at @s on attacker if entity @s[scores={saber=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[0.0,0.98,1.0],scale:2} ~0.5 ~1 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={saber=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{saber_tag:1b}}}}] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:2} ~0.5 ~1 ~0.5 -1 -1 -1 1 20

scoreboard players reset * random
scoreboard players reset * saber
