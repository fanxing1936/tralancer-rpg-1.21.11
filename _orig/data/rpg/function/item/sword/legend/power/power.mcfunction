effect clear @a[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] wither 
effect clear @a[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] darkness
effect clear @a[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] blindness
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run effect give @e[distance=0..2] glowing 5 3 true
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[1.0,1.0,1.0],scale:3} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 0.1 20
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
execute as @e at @s on attacker if entity @s[scores={power=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run summon wither_skull ~ ~5 ~ {Motion:[0d,-0.3d]}

execute as @a[scores={power_step=20..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] at @s run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:1} ~0.25 ~1 ~0.25 -0.5 -0.75 -0.5 0.1 5
execute as @a[scores={power_step=20..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] at @s run effect give @s speed 1 2 true
execute as @a[scores={power_step=20},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] at @s run playsound minecraft:block.trial_spawner.ominous_activate
execute as @e at @s on attacker if entity @s[scores={power=0..,power_step=20..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] at @s run summon armor_stand ^ ^0.3 ^2 {Invisible:1b,CustomName:'[{"text":"power_atk"}]',Invulnerable:1b}
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run tp @s ~ ~ ~ facing entity @p[scores={power_step=20..}]
execute as @e at @s on attacker if entity @s[scores={power=0..,power_step=20..},nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run scoreboard players reset @s power_step



scoreboard players reset * power

execute as @e[name=power_atk,type=armor_stand] anchored eyes at @s run particle sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 1 10 force
execute as @e[name=power_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 10 force
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-0.8  
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2.5] {Motion:[0d,1d,0d]}
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] if entity @e[name=power_atk,type=armor_stand,distance=..2] run tp @e[limit=1,sort=nearest] @e[name=power_atk,type=armor_stand,distance=..2,limit=1]
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] if entity @e[name=power_atk,type=armor_stand,distance=..2] run damage @e[limit=1,sort=nearest] 3 minecraft:player_attack by @s

execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless entity @a[distance=..50,nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run kill 
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run kill
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run kill


