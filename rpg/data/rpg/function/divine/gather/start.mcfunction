tag @s add rpg.lt.gathering
scoreboard players set @s rpg_lt_gather 0
scoreboard players add #next rpg_lt_owner 1
scoreboard players operation @s rpg_lt_owner = #next rpg_lt_owner
scoreboard players operation @a[tag=rpg.kabbalah.user,distance=..1,limit=1] rpg_lt_owner = #next rpg_lt_owner
clear @a[tag=rpg.kabbalah.user,distance=..1,limit=1] minecraft:iron_nugget[minecraft:custom_data~{rpg_true_cross:1b}] 1
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.ritual.life_tree.cross"],item:{id:"minecraft:iron_nugget",count:1,components:{"minecraft:custom_model_data":{floats:[1110001.0f]},"minecraft:enchantment_glint_override":1b}},item_display:"ground",view_range:0.8f,brightness:{block:15,sky:15},transformation:{translation:[0f,0.04f,0f],scale:[1.0f,1.0f,1.0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
particle minecraft:flash{color:16777215} ~ ~0.2 ~ 0 0 0 0 1 force
playsound minecraft:block.beacon.activate master @a[distance=..24] ~ ~ ~ 1 1.55
tellraw @a[tag=rpg.kabbalah.user,distance=..1,limit=1] ["",{"text":"[秘仪] ","color":"#D596F2","bold":true,"italic":false},{"text":"真·十字架在","color":"gray","bold":false,"italic":false},{"text":"Daath 节点","color":"#62D9E8","bold":true,"italic":false},{"text":"承接禁忌知识；十源质开始汇聚……","color":"gray","bold":false,"italic":false}]
tag @a[tag=rpg.kabbalah.user,distance=..1] remove rpg.kabbalah.user
