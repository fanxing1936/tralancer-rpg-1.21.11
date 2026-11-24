# 驱魔图腾
execute unless score @s rpg_sef matches 3.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　要原质第 3 阶才能做驱魔图腾","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank_rite"}] run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　主手要拿着空白圣具","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:shulker_shell[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 2.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　潜影壳不够（要 2）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:prismarine_shard[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 8.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　海晶碎片不够（要 8）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:shulker_shell[!minecraft:custom_data] 2
clear @s minecraft:prismarine_shard[!minecraft:custom_data] 8
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:alc/give/totem
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 1.2
scoreboard players add @s rpg_alc_made 1
tellraw @s ["",{"text":"[制器]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　做成：","color":"gray","bold":false,"italic":false},{"text":"[驱魔]","color":"#FFD85A","bold":true,"italic":false},{"text":"驱魔图腾","color":"#FFFFFF","bold":false,"italic":false}]
