# 核对利维坦之歌的材料：#ok 1 = 够
scoreboard players set #ok rpg_fg 0
execute unless score @s rpg_sef matches 6.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　原质要到第 6 阶才能锻[传说]","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　主手要拿着器胚","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_tear"}] 0
execute unless score #c rpg_fg matches 3.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　深海之泪不够（要 3）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 2.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　下界合金锭不够（要 2）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #c rpg_fg matches 6.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　残魂不够（要 6）","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players set #ok rpg_fg 1
