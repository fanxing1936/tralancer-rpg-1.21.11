execute if score @s devil matches 400.. run scoreboard players set @s devil 0
scoreboard players add @s devil 1
particle sculk_soul ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 1
execute if score @s devil matches 50 at @a[distance=..15] run particle minecraft:elder_guardian
execute if score @s devil matches 50..51 run playsound minecraft:entity.allay.death player @a[distance=..15]
execute if score @s devil matches 150 run summon armor_stand ^ ^ ^3 {Invisible:1b,CustomName:[{"text":"devil_attack"}],Invulnerable:1b,Tags:["rpg.boss.slash","rpg.boss.slash.new"]}
execute if score @s devil matches 150 run summon armor_stand ^3 ^ ^3 {Invisible:1b,CustomName:[{"text":"devil_attack"}],Invulnerable:1b,Tags:["rpg.boss.slash","rpg.boss.slash.new"]}
execute if score @s devil matches 150 run summon armor_stand ^-3 ^ ^3 {Invisible:1b,CustomName:[{"text":"devil_attack"}],Invulnerable:1b,Tags:["rpg.boss.slash","rpg.boss.slash.new"]}
execute if score @s devil matches 150 run playsound minecraft:item.mace.smash_air player @a[distance=..20]
execute if score @s devil matches 150 run execute as @e[type=minecraft:armor_stand,tag=rpg.boss.slash.new] at @s run tp @s ~ ~ ~ facing entity @a[distance=..20,limit=1,sort=random]
tag @e[type=minecraft:armor_stand,tag=rpg.boss.slash.new] remove rpg.boss.slash.new
execute if score @s devil matches 250 run effect give @s minecraft:instant_health 1 3 true
execute if score @s devil matches 250 run particle minecraft:sweep_attack ~5 ~1.2 ~5 -10 -1 -10 0 72 normal
execute if score @s devil matches 250 run playsound minecraft:entity.ghast.death player @a[distance=..15]
execute if score @s devil matches 250 run function rpg:entities/warden/pseudo_burst_players
execute if score @s devil matches 250 as @a[distance=..10] at @s run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 24
execute if score @s devil matches 350 as @a[distance=..10] at @s run summon lightning_bolt ~ ~ ~
execute if score @s devil matches 350 as @a[distance=..10] at @s run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 16
execute if score @s devil matches 350 as @a[distance=..10] at @s run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 16
execute if score @s devil matches 390 run function rpg:entities/warden/pseudo_burst_minions
execute if score @s devil matches 390 run summon vindicator ~2 ~ ~ {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new","rpg.boss.minion2"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute if score @s devil matches 390 positioned ~2 ~ ~ run function rpg:entities/warden/pseudo_minion_stamp
execute if score @s devil matches 390 run summon vindicator ~-2 ~ ~ {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new","rpg.boss.minion2"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute if score @s devil matches 390 positioned ~-2 ~ ~ run function rpg:entities/warden/pseudo_minion_stamp
execute if score @s devil matches 390 run summon vindicator ~ ~ ~2 {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new","rpg.boss.minion2"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute if score @s devil matches 390 positioned ~ ~ ~2 run function rpg:entities/warden/pseudo_minion_stamp
execute if score @s devil matches 390 run summon vindicator ~ ~ ~-2 {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new","rpg.boss.minion2"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute if score @s devil matches 390 positioned ~ ~ ~-2 run function rpg:entities/warden/pseudo_minion_stamp
