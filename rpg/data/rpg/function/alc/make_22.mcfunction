# 替死人偶
execute unless score @s rpg_sef matches 2.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　要原质第 2 阶才能做替死人偶","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank_rite"}] run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　主手要拿着空白圣具","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:string[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 12.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　蛛丝不够（要 12）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:phantom_membrane[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 2.. run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　幻翼膜不够（要 2）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:string[!minecraft:custom_data] 12
clear @s minecraft:phantom_membrane[!minecraft:custom_data] 2
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:alc/give/doll
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 1.2
scoreboard players add @s rpg_alc_made 1
tellraw @s ["",{"text":"[制器]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　做成：","color":"gray","bold":false,"italic":false},{"text":"[驱魔]","color":"#FFD85A","bold":true,"italic":false},{"text":"替死人偶","color":"#FFFFFF","bold":false,"italic":false}]
