execute as @e[nbt={Tags:["devil"]}] at @s run effect give @s minecraft:invisibility 1 1 true
execute as @e[nbt={Tags:["devil"]}] at @s run particle large_smoke ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 1
execute as @e[nbt={Tags:["devil"]}] at @s run particle squid_ink ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 5
execute as @e on attacker if entity @e[nbt={Tags:["devil"]}] at @s run effect clear @s minecraft:invisibility
execute as @e on attacker if entity @e[nbt={Tags:["devil"]}] at @s run effect give @s minecraft:glowing 1 1 true

execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 200.. run scoreboard players set @s devil 0
scoreboard players add @e[nbt={Tags:["devil"]}] devil 1

execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 50..51 run effect give @a[distance=..15] minecraft:blindness 5 10 true
execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 50 at @a[distance=..15] run particle minecraft:elder_guardian
execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 50..51 run playsound minecraft:entity.allay.death player @a[distance=..15]

execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 100 run effect give @a[distance=..15] minecraft:nausea 5 2 true

execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 150..151 run playsound minecraft:entity.allay.ambient_with_item player @a[distance=..15]
execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 150..151 run effect give @s minecraft:instant_health 1 1 true 


execute as @e[nbt={Tags:["devil"]}] at @s run effect give @a[distance=..15] minecraft:darkness 5 10 true
execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 60 run playsound minecraft:entity.vex.death player @a[distance=..15]
execute as @e[nbt={Tags:["devil"]}] at @s if score @s devil matches 180 run playsound minecraft:entity.vex.death player @a[distance=..15]

execute as @e[nbt={Tags:["devil"]}] at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_tag:1b}}}}] run effect give @e[distance=..1,limit=1] minecraft:instant_damage 1 0 true
execute as @e[nbt={Tags:["devil"]}] at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_tag:1b}}}}] run effect clear @e[distance=..1,limit=1] minecraft:invisibility

execute as @e[nbt={Tags:["devil"]}] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute as @e[nbt={Tags:["devil"]}] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10


execute as @e[nbt={Tags:["boss"]}] at @s store result bossbar minecraft:devil value run data get entity @s Health
execute as @e[nbt={Tags:["devil","boss"]}] at @s if score @s devil matches 150 store result score @s random run random value 1..3
execute as @e[nbt={Tags:["devil","boss"]},scores={random=1}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.hurt player @a[distance=..15]
execute as @e[nbt={Tags:["devil","boss"]},scores={random=1}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run summon vindicator ~ ~ ~ {Johnny:1,Health:50,Silent:1b,Tags:["devil"],active_effects:[{id:speed,duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:attack_knockback,base:2f},{id:"generic.max_health",base:100f}]}
execute as @e[nbt={Tags:["devil","boss"]},scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.death player @a[distance=..15]
execute as @e[nbt={Tags:["devil","boss"]},scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s slowness 3 255 true
execute as @e[nbt={Tags:["devil","boss"]},scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s glowing 3 255 true
execute as @e[nbt={Tags:["devil","boss"]},scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run damage @s 10 minecraft:wither
scoreboard players reset * random
execute as @e[nbt={Tags:["devil","boss"]}] at @s if score @s devil matches 150..151 run effect give @s minecraft:instant_health 1 3 true 
execute as @e[nbt={Tags:["devil","boss"]}] at @s if score @s devil matches 100..105 at @a[distance=..20] run summon evoker_fangs
execute as @e[nbt={Tags:["devil","boss"]}] at @s if score @s devil matches 40 if entity @a[distance=..5] run playsound minecraft:entity.vex.charge player @a[distance=..15]
execute as @e[nbt={Tags:["devil","boss"]}] at @s if score @s devil matches 50 if entity @a[distance=..5] run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 1000
execute as @e[nbt={Tags:["devil","boss"]}] at @s if score @s devil matches 50 if entity @a[distance=..5] run summon minecraft:creeper ~ ~1 ~ {"ExplosionRadius":8,"Fuse":0}

##二阶段
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 400.. run scoreboard players set @s devil 0
scoreboard players add @e[nbt={Tags:["devil2","boss"]}] devil 1
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[nbt={Tags:["devil2"]}] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[nbt={Tags:["devil2"]}] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[nbt={Tags:["devil2","boss"]}] run effect give @e[limit=1] minecraft:wither 5 3 true
scoreboard players reset * devil_hurt

execute as @e[nbt={Tags:["devil2"]}] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute as @e[nbt={Tags:["devil2"]}] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10


execute as @e[nbt={Tags:["devil2","boss"]}] at @s run particle sculk_soul ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 1

execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 50 at @a[distance=..15] run particle minecraft:elder_guardian
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 50..51 run playsound minecraft:entity.allay.death player @a[distance=..15]
##斩击
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 150 run summon armor_stand ^ ^ ^3 {Invisible:1b,CustomName:'[{"text":"devil_attack"}]',Invulnerable:1b}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 150 run summon armor_stand ^3 ^ ^3 {Invisible:1b,CustomName:'[{"text":"devil_attack"}]',Invulnerable:1b}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 150 run summon armor_stand ^-3 ^ ^3 {Invisible:1b,CustomName:'[{"text":"devil_attack"}]',Invulnerable:1b}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 150 run playsound minecraft:item.mace.smash_air player @a[distance=..20]
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 150 run execute as @e[name=devil_attack,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @a[distance=..20,limit=1,sort=random]


execute as @e[name=devil_attack,type=armor_stand] anchored eyes at @s run particle minecraft:sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 0 20 force
execute as @e[name=devil_attack,type=armor_stand] anchored eyes at @s run particle large_smoke ~0.5 ~1.2 ~0.5 -1 -1 -1 0.2 20 force
execute as @e[name=devil_attack,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^1  
execute as @e[name=devil_attack,type=armor_stand] anchored feet at @s run damage @e[limit=1,sort=nearest,distance=0.1..3,tag=ashes] 20 minecraft:outside_border
execute as @e[name=devil_attack,type=armor_stand] anchored feet at @s unless entity @e[distance=..50,nbt={Tags:["devil2"]}] run kill 


execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 250 run effect give @s minecraft:instant_health 1 3 true 
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 250 run particle minecraft:sweep_attack ~5 ~1.2 ~5 -10 -1 -10 0 300 force
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 250 run playsound minecraft:entity.ghast.death player @a[distance=..15]
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 250 as @a[distance=..10] at @s run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":3,"Fuse":0}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 250 as @a[distance=..10] at @s run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 100


execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 350 as @a[distance=..10] at @s run summon lightning_bolt ~ ~ ~
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 350 as @a[distance=..10] at @s run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 350 as @a[distance=..10] at @s run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50


execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run execute as @e[nbt={Tags:["devil2","tick"]}] at @s run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":4,"Fuse":0}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run execute as @e[nbt={Tags:["devil2","tick"]}] at @s run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 100 
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run execute as @e[nbt={Tags:["devil2","tick"]}] at @s run kill
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run summon vindicator ~2 ~ ~ {Johnny:1,Health:100,Tags:["devil2","tick"],HandItems:[{id:netherite_sword,components:{custom_model_data:1110007},count:1}],HandDropChances:[0f],attributes:[{id:"generic.max_health",base:100f}]}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run summon vindicator ~-2 ~ ~ {Johnny:1,Health:100,Tags:["devil2","tick"],HandItems:[{id:netherite_sword,components:{custom_model_data:1110007},count:1}],HandDropChances:[0f],attributes:[{id:"generic.max_health",base:100f}]}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run summon vindicator ~ ~ ~2 {Johnny:1,Health:100,Tags:["devil2","tick"],HandItems:[{id:netherite_sword,components:{custom_model_data:1110007},count:1}],HandDropChances:[0f],attributes:[{id:"generic.max_health",base:100f}]}
execute as @e[nbt={Tags:["devil2","boss"]}] at @s if score @s devil matches 390 run summon vindicator ~ ~ ~-2 {Johnny:1,Health:100,Tags:["devil2","tick"],HandItems:[{id:netherite_sword,components:{custom_model_data:1110007},count:1}],HandDropChances:[0f],attributes:[{id:"generic.max_health",base:100f}]}

