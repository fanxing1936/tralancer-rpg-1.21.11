execute if entity @s[tag=rpg.lt.yesod] run tellraw @a[tag=rpg.kabbalah.user,distance=..1,limit=1] ["",{"text":"[源质·09] ","color":"#D596F2","bold":true,"italic":false},{"text":"基础","color":"#D596F2","bold":true,"italic":false},{"text":"已经归位。","color":"gray","bold":false,"italic":false}]
execute if entity @s[tag=rpg.lt.yesod] run tag @a[tag=rpg.kabbalah.user,distance=..1] remove rpg.kabbalah.user
execute if entity @s[tag=rpg.lt.yesod] run return 0
tag @s add rpg.lt.yesod
scoreboard players add @s rpg_lt_fill 1
clear @a[tag=rpg.kabbalah.user,distance=..1,sort=nearest,limit=1] minecraft:purple_dye[minecraft:custom_data~{rpg_sephirah:9b}] 1
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.ritual.life_tree.prop","rpg.ritual.life_tree.prop.yesod"],item:{id:"minecraft:purple_dye",count:1,components:{"minecraft:enchantment_glint_override":1b}},item_display:"ground",view_range:0.65f,shadow_radius:0.15f,shadow_strength:0.38f,brightness:{block:15,sky:12},transformation:{translation:[0f,0.035f,0f],scale:[0.72f,0.72f,0.72f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
particle dust{color:[0.522,0.220,0.678],scale:1.25} ~ ~0.10 ~ 0.40 0.03 0.40 0.02 22
particle end_rod ~ ~0.12 ~ 0.28 0.05 0.28 0.02 12
playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..16] ~ ~ ~ 0.65 1.10
tellraw @a[tag=rpg.kabbalah.user,distance=..1,limit=1] ["",{"text":"[源质·09] ","color":"#D596F2","bold":true,"italic":false},{"text":"基础","color":"#D596F2","bold":true,"italic":false},{"text":"归位。","color":"gray","bold":false,"italic":false},{"text":"　完成度 ","color":"gray","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_lt_fill"},"color":"#D596F2","bold":true,"italic":false},{"text":"/10","color":"dark_gray","bold":false,"italic":false}]
execute if score @s rpg_lt_fill matches 10.. at @s run function rpg:ritual/life_tree/complete
tag @a[tag=rpg.kabbalah.user,distance=..1] remove rpg.kabbalah.user
