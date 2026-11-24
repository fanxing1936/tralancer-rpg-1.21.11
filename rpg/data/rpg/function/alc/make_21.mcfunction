# 浓缩驱魔圣水
execute unless score @s rpg_ex_rites matches 3.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　要完成过 3 次裁决才能做浓缩驱魔圣水","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"vial"}] run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　主手要拿着空瓶","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s *[minecraft:custom_data~{rite_tag:1b},!minecraft:custom_data~{rpg_strong_water:1b}] 0
execute unless score #c rpg_fg matches 2.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　驱魔圣水不够（要 2）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_bronze"}] 0
execute unless score #c rpg_fg matches 1.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　圣殿铜不够（要 1）","color":"#C04A3C","bold":false,"italic":false}]
clear @s *[minecraft:custom_data~{rite_tag:1b},!minecraft:custom_data~{rpg_strong_water:1b}] 2
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_bronze"}] 1
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:inquest/give/strong_water
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40
playsound minecraft:block.brewing_stand.brew player @s ~ ~ ~ 1 1
scoreboard players add @s rpg_alc_made 1
tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　做成：","color":"gray","bold":false,"italic":false},{"text":"[驱魔]","color":"#FFD85A","bold":true,"italic":false},{"text":"浓缩驱魔圣水","color":"#FFFFFF","bold":false,"italic":false}]
