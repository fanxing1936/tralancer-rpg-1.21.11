execute if entity @e[tag=devil] run function rpg:entities/warden/warden/g0
execute if entity @e[tag=devil,limit=1] run function rpg:entities/warden/warden/h1

execute as @e[tag=devil] at @s if score @s devil matches 200.. run scoreboard players set @s devil 0
scoreboard players add @e[tag=devil] devil 1

execute if entity @e[tag=devil] run function rpg:entities/warden/warden/g1


execute as @e[tag=boss] at @s store result bossbar minecraft:devil value run data get entity @s Health
execute as @e[tag=devil,tag=boss] at @s if score @s devil matches 150 store result score @s random run random value 1..3
execute as @e[tag=devil,tag=boss,scores={random=1}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.hurt player @a[distance=..15]
execute as @e[tag=devil,tag=boss,scores={random=1}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run summon vindicator ~ ~ ~ {Johnny:1,Health:50,Silent:1b,Tags:["devil"],active_effects:[{id:speed,duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:attack_knockback,base:2f},{id:"max_health",base:100f}]}
execute as @e[tag=devil,tag=boss,scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.death player @a[distance=..15]
execute as @e[tag=devil,tag=boss,scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s slowness 3 255 true
execute as @e[tag=devil,tag=boss,scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s glowing 3 255 true
execute as @e[tag=devil,tag=boss,scores={random=2}] at @s if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run damage @s 10 minecraft:wither
scoreboard players reset * random
execute if entity @e[tag=devil,tag=boss] run function rpg:entities/warden/warden/g2

##二阶段
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 400.. run scoreboard players set @s devil 0
scoreboard players add @e[type=minecraft:vindicator,tag=devil2,tag=boss] devil 1
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2,tag=boss] run effect give @e[limit=1] minecraft:wither 5 3 true
scoreboard players reset * devil_hurt

execute as @e[type=minecraft:vindicator,tag=devil2] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute as @e[type=minecraft:vindicator,tag=devil2] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10


execute if entity @e[type=minecraft:vindicator,tag=devil2,tag=boss] run function rpg:entities/warden/warden/g3


execute as @e[name=devil_attack,type=armor_stand] anchored eyes at @s run particle minecraft:sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 0 20 force
execute as @e[name=devil_attack,type=armor_stand] anchored eyes at @s run particle large_smoke ~0.5 ~1.2 ~0.5 -1 -1 -1 0.2 20 force
execute as @e[name=devil_attack,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^1  
execute as @e[name=devil_attack,type=armor_stand] anchored feet at @s run damage @e[limit=1,sort=nearest,distance=0.1..3,tag=ashes] 20 minecraft:outside_border
execute as @e[name=devil_attack,type=armor_stand] anchored feet at @s unless entity @e[type=minecraft:vindicator,distance=..50,tag=devil2] run kill 


execute if entity @e[type=minecraft:vindicator,tag=devil2,tag=boss] run function rpg:entities/warden/warden/g4

