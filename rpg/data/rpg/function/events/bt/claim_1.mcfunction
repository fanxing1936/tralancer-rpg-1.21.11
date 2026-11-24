# 领取第 1 条悬赏（as 玩家）
execute if score @s rpg_bt_c1 matches 1 run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　这条已经领过了","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 1 unless score @s rpg_bt_p1 matches 20.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 2 unless score @s rpg_bt_p1 matches 15.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 3 unless score @s rpg_bt_p1 matches 8.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 4 unless score @s rpg_bt_p1 matches 15.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 5 unless score @s rpg_bt_p1 matches 2.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 6 store result score #c rpg_ev run clear @s minecraft:iron_ingot[!minecraft:custom_data] 0
execute if score @s rpg_bt_t1 matches 6 unless score #c rpg_ev matches 16.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　铁锭不够（要 16）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 6 run clear @s minecraft:iron_ingot[!minecraft:custom_data] 16
execute if score @s rpg_bt_t1 matches 7 store result score #c rpg_ev run clear @s minecraft:gold_ingot[!minecraft:custom_data] 0
execute if score @s rpg_bt_t1 matches 7 unless score #c rpg_ev matches 6.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　金锭不够（要 6）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 7 run clear @s minecraft:gold_ingot[!minecraft:custom_data] 6
execute if score @s rpg_bt_t1 matches 8 store result score #c rpg_ev run clear @s minecraft:bone 0
execute if score @s rpg_bt_t1 matches 8 unless score #c rpg_ev matches 24.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　骸骨不够（要 24）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 8 run clear @s minecraft:bone 24
execute if score @s rpg_bt_t1 matches 9 store result score #c rpg_ev run clear @s minecraft:string 0
execute if score @s rpg_bt_t1 matches 9 unless score #c rpg_ev matches 24.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　蛛丝不够（要 24）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 9 run clear @s minecraft:string 24
execute if score @s rpg_bt_t1 matches 10 store result score #c rpg_ev run clear @s minecraft:gunpowder 0
execute if score @s rpg_bt_t1 matches 10 unless score #c rpg_ev matches 12.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　火药不够（要 12）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 10 run clear @s minecraft:gunpowder 12
execute if score @s rpg_bt_t1 matches 11 store result score #c rpg_ev run clear @s minecraft:blaze_powder 0
execute if score @s rpg_bt_t1 matches 11 unless score #c rpg_ev matches 10.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　烈焰粉不够（要 10）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 11 run clear @s minecraft:blaze_powder 10
execute if score @s rpg_bt_t1 matches 12 store result score #c rpg_ev run clear @s minecraft:ender_pearl 0
execute if score @s rpg_bt_t1 matches 12 unless score #c rpg_ev matches 4.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　末影珍珠不够（要 4）","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 12 run clear @s minecraft:ender_pearl 4
execute if score @s rpg_bt_t1 matches 13 unless score @s rpg_bt_p1 matches 5.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 14 unless score @s rpg_bt_p1 matches 30.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_t1 matches 15 unless score @s rpg_bt_p1 matches 2.. run return run tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　还没完成","color":"gray","bold":false,"italic":false}]
scoreboard players set @s rpg_bt_c1 1
function rpg:events/bt/reward
