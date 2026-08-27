give @s minecraft:gold_ingot[custom_name=["",{"text":"[item]","italic":false,"color":"gold","bold":true},{"text":"黄金","italic":false,"bold":false}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"上等的","italic":false,"color":"white"},{"text":"[物品]","italic":false,"color":"gold","bold":true}],["",{"text":"好用的材料","italic":false,"color":"white"}],["",{"text":"+------------------+","italic":false,"color":"white"}]],custom_data={gold_tag:1b}] 4
scoreboard players set @s rpg_pr_pending 0
tellraw @s ["",{"text":"[恩赐]","color":"#D4AF37","bold":true,"italic":false},{"text":"祷告已被垂听。获得：","color":"#AAB4C3","bold":false,"italic":false},{"text":"黄金","color":"#AAB4C3","bold":false,"italic":false},{"text":" ×4","color":"#AAB4C3","bold":false,"italic":false}]
particle minecraft:end_rod ~ ~1 ~ 0.35 0.55 0.35 0.02 8 normal @s
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.5 1.5
