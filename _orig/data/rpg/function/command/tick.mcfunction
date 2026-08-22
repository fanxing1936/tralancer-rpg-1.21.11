function rpg:item/chestplate/off


function rpg:item/sword/off/off

function rpg:item/bow/off


function rpg:item/sword/main/sweep/sweep_trigger
function rpg:item/sword/main/sweep/sweep_into

function rpg:item/sword/main/flame/flame_into
function rpg:item/sword/main/flame/flame_trigger

function rpg:item/sword/main/wind/wind_into
function rpg:item/sword/main/wind/wind_trigger

function rpg:item/bow/legend/bubble/bubble
function rpg:item/bow/legend/burn/burn
function rpg:item/bow/legend/hunter/hunter




function rpg:command/com




function rpg:task/trial/trial

function rpg:loot/loot

function rpg:level/player


#生物检测

execute as @e[type=#minecraft:skeletons,tag=!skeleton] at @s store result score @s random run random value 1..20
execute as @e[type=#minecraft:skeletons,tag=!skeleton,scores={random=10}] at @s run summon stray ~ ~ ~ {Health:30,ArmorItems:[{},{},{id:chainmail_chestplate,components:{trim:{pattern:wayfinder,material:lapis}},count:1},{id:chainmail_helmet,components:{trim:{pattern:eye,material:lapis}},count:1}],ArmorDropChances:[0f,0f,0f,0f],attributes:[{id:"generic.max_health",base:30f}]}
execute as @e[type=#minecraft:skeletons,tag=!skeleton,scores={random=11}] at @s run summon skeleton_horse ~ ~ ~ {Passengers:[{id:skeleton,Health:30,ArmorItems:[{},{},{id:iron_chestplate,components:{trim:{pattern:silence,material:quartz}},count:1},{id:iron_helmet,components:{trim:{pattern:silence,material:quartz}},count:1}],ArmorDropChances:[0f,0f,0f,0f],attributes:[{id:"generic.max_health",base:30f}]}]}
execute as @e[type=#minecraft:skeletons,tag=!skeleton,scores={random=12}] at @s run summon wither_skeleton ~ ~ ~ {Health:40,HandItems:[{id:netherite_sword,count:1}],HandDropChances:[0f],ArmorItems:[{},{},{id:netherite_chestplate,components:{trim:{pattern:silence,material:netherite}},count:1},{id:netherite_helmet,components:{trim:{pattern:silence,material:netherite}},count:1}],ArmorDropChances:[0f,0f,0f,0f],attributes:[{id:"generic.max_health",base:40f}]}
loot replace entity @e[type=#minecraft:skeletons,tag=!skeleton] weapon.mainhand loot rpg:armor/bow
loot replace entity @e[type=#minecraft:skeletons,tag=!skeleton] armor.chest loot rpg:armor/chestplate
loot replace entity @e[type=#minecraft:skeletons,tag=!skeleton] armor.head loot rpg:armor/helmet
loot replace entity @e[type=#minecraft:skeletons,tag=!skeleton] armor.legs loot rpg:armor/leggings
loot replace entity @e[type=#minecraft:skeletons,tag=!skeleton] armor.feet loot rpg:armor/boots
tag @e[type=#minecraft:skeletons] add skeleton


execute as @e[type=#minecraft:zombies,tag=!zombie] at @s store result score @s random run random value 1..20
execute as @e[type=#minecraft:zombies,tag=!zombie,scores={random=8}] at @s run summon zombie ~ ~ ~ {Health:50,HandItems:[{id:iron_sword,count:1}],ArmorItems:[{},{},{id:chainmail_chestplate,components:{trim:{pattern:eye,material:redstone}},count:1},{id:target,count:1}],HandDropChances:[0f],ArmorDropChances:[0f,0f,0f,0f],attributes:[{id:"generic.attack_damage",base:4f},{id:"generic.scale",base:1.1f},{id:"generic.max_health",base:50f}]}
execute as @e[type=#minecraft:zombies,tag=!zombie,scores={random=9}] at @s run summon zombie ~ ~ ~ {Health:40,ArmorItems:[{},{},{id:leather_chestplate,components:{trim:{pattern:silence,material:copper},dyed_color:{rgb:4673362}},count:1},{id:mangrove_roots,count:1}],ArmorDropChances:[0f,0f,0f,0f],attributes:[{id:"generic.attack_damage",base:2f},{id:"generic.armor",base:5f},{id:"generic.max_health",base:40f}],Passengers:[{id:zombie,IsBaby:1}]}
execute as @e[type=#minecraft:zombies,tag=!zombie,scores={random=10}] at @s run summon zombie_villager ~ ~ ~ {VillagerData:{type:plains,profession:armorer,level:5},Health:40,ArmorItems:[{},{},{id:chainmail_chestplate,components:{trim:{pattern:ward,material:quartz}},count:1},{id:cobweb,count:1}],ArmorDropChances:[0f,0f,0f,0f],attributes:[{id:"generic.attack_damage",base:2f},{id:"generic.armor",base:5f},{id:"generic.max_health",base:40f}],Passengers:[{id:zombie_villager,VillagerData:{type:plains,profession:farmer,level:2},IsBaby:1}]}
execute as @e[type=#minecraft:zombies,tag=!zombie,scores={random=14..15}] at @s run summon zombie ~ ~ ~ {Passengers:[{id:zombie,Passengers:[{id:zombie,Passengers:[{id:zombie,Passengers:[{id:zombie}]}]}]}]}
execute as @e[type=#minecraft:zombies,tag=!zombie,scores={random=10}] at @s run summon zombie ~ ~ ~ {Health:100,attributes:[{id:"generic.scale",base:3f},{id:"generic.attack_damage",base:5f},{id:"generic.attack_speed",base:1f},{id:"generic.max_health",base:100f}]}
loot replace entity @e[type=#minecraft:zombies,tag=!zombie] weapon.mainhand loot rpg:armor/sword
loot replace entity @e[type=#minecraft:zombies,tag=!zombie] armor.chest loot rpg:armor/chestplate
loot replace entity @e[type=#minecraft:zombies,tag=!zombie] armor.head loot rpg:armor/helmet
loot replace entity @e[type=#minecraft:zombies,tag=!zombie] armor.legs loot rpg:armor/leggings
loot replace entity @e[type=#minecraft:zombies,tag=!zombie] armor.feet loot rpg:armor/boots
tag @e[type=#minecraft:zombies] add zombie

execute as @e[type=minecraft:creeper,tag=!creeper] at @s store result score @s random run random value 1..10
execute as @e[type=minecraft:creeper,tag=!creeper,scores={random=10}] at @s run summon creeper ~ ~ ~ {powered:1,ExplosionRadius:5,Health:30,attributes:[{id:"generic.scale",base:1.3f},{id:"generic.max_health",base:30f}]}
execute as @e[type=minecraft:creeper,tag=!creeper,scores={random=9}] at @s run summon creeper ~ ~ ~ {ExplosionRadius:1.5,Health:10,fuse:10,attributes:[{id:"generic.scale",base:0.5f},{id:"generic.max_health",base:10f}]}
execute as @e[type=minecraft:creeper,tag=!creeper,scores={random=9}] at @s run summon creeper ~ ~ ~ {ExplosionRadius:1.5,Health:10,fuse:10,attributes:[{id:"generic.scale",base:0.5f},{id:"generic.max_health",base:10f}]}
execute as @e[type=minecraft:creeper,tag=!creeper,scores={random=9}] at @s run summon creeper ~ ~ ~ {ExplosionRadius:1.5,Health:10,fuse:10,attributes:[{id:"generic.scale",base:0.5f},{id:"generic.max_health",base:10f}]}
tag @e[type=minecraft:creeper] add creeper

