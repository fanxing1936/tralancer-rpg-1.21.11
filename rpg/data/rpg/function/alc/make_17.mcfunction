# 血战药水
execute unless score @s rpg_sef matches 5.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　要原质第 5 阶才能做血战药水","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"vial"}] run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　主手要拿着空瓶","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:blaze_powder[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 6.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　烈焰粉不够（要 6）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:redstone[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 6.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　红石粉不够（要 6）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #c rpg_fg matches 3.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　残魂不够（要 3）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_core"}] 0
execute unless score #c rpg_fg matches 1.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　熔核不够（要 1）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:blaze_powder[!minecraft:custom_data] 6
clear @s minecraft:redstone[!minecraft:custom_data] 6
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 3
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_core"}] 1
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
loot give @s loot rpg:potion/frenzy
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40
playsound minecraft:block.brewing_stand.brew player @s ~ ~ ~ 1 1
scoreboard players add @s rpg_alc_made 1
tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　做成：","color":"gray","bold":false,"italic":false},{"text":"[传说]","color":"#FFAA00","bold":true,"italic":false},{"text":"血战药水","color":"#FFFFFF","bold":false,"italic":false}]
