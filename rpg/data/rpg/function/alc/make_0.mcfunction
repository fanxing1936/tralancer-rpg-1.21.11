# 精血药水
execute unless score @s rpg_sef matches 1.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　要原质第 1 阶才能做精血药水","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"vial"}] run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　主手要拿着空瓶","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:rotten_flesh[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 8.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　腐肉不够（要 8）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:spider_eye[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 2.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　蜘蛛眼不够（要 2）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:rotten_flesh[!minecraft:custom_data] 8
clear @s minecraft:spider_eye[!minecraft:custom_data] 2
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
loot give @s loot rpg:potion/blood
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40
playsound minecraft:block.brewing_stand.brew player @s ~ ~ ~ 1 1
scoreboard players add @s rpg_alc_made 1
tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　做成：","color":"gray","bold":false,"italic":false},{"text":"[勇者]","color":"#00AAAA","bold":true,"italic":false},{"text":"精血药水","color":"#FFFFFF","bold":false,"italic":false}]
