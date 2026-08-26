scoreboard players add @s rpg_ex_xp 12
execute if score #floor rpg_end_tmp matches ..14 run give @s minecraft:diamond 1
execute if score #floor rpg_end_tmp matches 15..29 run give @s minecraft:netherite_scrap 1
execute if score #floor rpg_end_tmp matches 30..49 run give @s minecraft:netherite_scrap 2
execute if score #floor rpg_end_tmp matches 30..49 run give @s minecraft:echo_shard 2
execute if score #floor rpg_end_tmp matches 50.. run give @s minecraft:netherite_ingot 1
execute if score #floor rpg_end_tmp matches 50.. run give @s minecraft:enchanted_golden_apple 1
tellraw @s ["",{"text":"[领主宝库] ","color":"#D4AF37","bold":true,"italic":false},{"text":"额外获得 Boss 层战利品与 12 点驱魔阅历。","color":"#FFF2A8","bold":false,"italic":false}]
