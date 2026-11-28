# 每秒（as/at 恶魔阵营的玩家）：圣水烫人；在圣卫面前拿罪器、罪印就暴露
execute if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,distance=..4] run damage @s 2 minecraft:magic
execute if score @s rpg_dm_exp matches 1.. run scoreboard players remove @s rpg_dm_exp 1
execute if score @s rpg_dm_exp matches 1 run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  圣卫不再追查你了。通缉令撤下了。","color":"#E6DFCF","bold":false,"italic":false}]
execute if score @s rpg_dm_exp matches ..0 if entity @e[tag=rpg.tw.guard,distance=..12] run function rpg:town/demon/check_held
