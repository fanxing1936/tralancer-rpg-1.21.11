# 17 行原本各自扫一遍全实体表找 @e[type=minecraft:vindicator,tag=devil2,tag=boss]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 250 run effect give @s minecraft:instant_health 1 3 true 
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 250 run particle minecraft:sweep_attack ~5 ~1.2 ~5 -10 -1 -10 0 300 force
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 250 run playsound minecraft:entity.ghast.death player @a[distance=..15]
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 250 run function rpg:entities/warden/pseudo_burst_players
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 250 as @a[distance=..10] at @s run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 100


execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 350 as @a[distance=..10] at @s run summon lightning_bolt ~ ~ ~
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 350 as @a[distance=..10] at @s run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 350 as @a[distance=..10] at @s run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50


execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 run function rpg:entities/warden/pseudo_burst_minions
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 run summon vindicator ~2 ~ ~ {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 positioned ~2 ~ ~ run function rpg:entities/warden/pseudo_minion_stamp
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 run summon vindicator ~-2 ~ ~ {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 positioned ~-2 ~ ~ run function rpg:entities/warden/pseudo_minion_stamp
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 run summon vindicator ~ ~ ~2 {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 positioned ~ ~ ~2 run function rpg:entities/warden/pseudo_minion_stamp
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 run summon vindicator ~ ~ ~-2 {Johnny:1,Health:100,Tags:["devil2","tick","rpg.pseudo_boom.minion_new"],attributes:[{id:"max_health",base:100f}],equipment:{mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{mainhand:0f}}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 390 positioned ~ ~ ~-2 run function rpg:entities/warden/pseudo_minion_stamp
