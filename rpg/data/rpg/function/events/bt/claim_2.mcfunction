# 领取第 2 条悬赏（as 玩家）
execute if score @s rpg_bt_c2 matches 1 run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　这条已经领过了","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 1 unless score @s rpg_bt_p2 matches 20.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 2 unless score @s rpg_bt_p2 matches 15.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 3 unless score @s rpg_bt_p2 matches 8.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 4 unless score @s rpg_bt_p2 matches 15.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 5 unless score @s rpg_bt_p2 matches 2.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 6 store result score #c rpg_ev run clear @s minecraft:iron_ingot[!minecraft:custom_data] 0
execute if score @s rpg_bt_t2 matches 6 unless score #c rpg_ev matches 16.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　铁锭不够（要 16）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 6 run clear @s minecraft:iron_ingot[!minecraft:custom_data] 16
execute if score @s rpg_bt_t2 matches 7 store result score #c rpg_ev run clear @s minecraft:gold_ingot[!minecraft:custom_data] 0
execute if score @s rpg_bt_t2 matches 7 unless score #c rpg_ev matches 6.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　金锭不够（要 6）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 7 run clear @s minecraft:gold_ingot[!minecraft:custom_data] 6
execute if score @s rpg_bt_t2 matches 8 store result score #c rpg_ev run clear @s minecraft:bone[!minecraft:custom_data] 0
execute if score @s rpg_bt_t2 matches 8 unless score #c rpg_ev matches 24.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　骸骨不够（要 24）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t2 matches 8 run clear @s minecraft:bone[!minecraft:custom_data] 24
scoreboard players set @s rpg_bt_c2 1
function rpg:events/bt/reward
