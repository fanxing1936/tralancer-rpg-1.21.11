# 召出一根藤蔓（位置=根部）。朝向随机，免得一排藤蔓长得一模一样。
summon minecraft:armor_stand ~ ~ ~ {Marker:1b,Invisible:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,Tags:["rpg.luv.root","rpg.luv.new","rpg.luv.spawning"]}
execute store result entity @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv.spawning,limit=1,sort=nearest] Rotation[0] float 1 run random value -180..179
scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv.spawning,limit=1,sort=nearest] rpg_luv_l 200
execute as @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv.spawning,limit=1,sort=nearest] at @s run function rpg:lucifer_vine/dress
tag @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv.spawning] remove rpg.luv.spawning
