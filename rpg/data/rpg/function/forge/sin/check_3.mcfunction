# 核对第 3 柱（亚巴顿）的材料：#ok 1 = 够
function rpg:forge/sin/need_3
scoreboard players set #ok rpg_fg 0
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　主手要拿着器胚","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:nether_star[minecraft:custom_data~{rpg_weapon_core:1b,rpg_lord:3}] 0
execute unless score #c rpg_fg matches 1.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　没有亚巴顿的武器核心（驱魔裁决选「消灭」取得）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sin_shard",rpg_lord:3}] 0
execute unless score #c rpg_fg >= #need_s rpg_fg run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　亚巴顿的罪印碎片不够","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 0
execute unless score #c rpg_fg >= #need_n rpg_fg run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　下界合金锭不够","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #c rpg_fg matches 8.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　残魂不够（要 8 枚）","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players set #ok rpg_fg 1
