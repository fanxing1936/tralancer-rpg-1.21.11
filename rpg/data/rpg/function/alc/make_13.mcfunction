# 烈焰药水
execute unless score @s rpg_sef matches 3.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　要原质第 3 阶才能做烈焰药水","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"vial"}] run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　主手要拿着空瓶","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:blaze_powder[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 4.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　烈焰粉不够（要 4）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:gunpowder[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 4.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　火药不够（要 4）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #c rpg_fg matches 1.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　残魂不够（要 1）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:blaze_powder[!minecraft:custom_data] 4
clear @s minecraft:gunpowder[!minecraft:custom_data] 4
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 1
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
loot give @s loot rpg:potion/blaze
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40
playsound minecraft:block.brewing_stand.brew player @s ~ ~ ~ 1 1
scoreboard players add @s rpg_alc_made 1
tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　做成：","color":"gray","bold":false,"italic":false},{"text":"[史诗]","color":"#B85CF0","bold":true,"italic":false},{"text":"烈焰药水","color":"#FFFFFF","bold":false,"italic":false}]
