# 蔓延。放着不管，一个村子会慢慢烂掉。
# 每 400 刻一拍，一拍只挑一个空缺者向外伸手 —— 绝不整场扫村民。
scoreboard players set #spread rpg_vac 0
execute as @e[type=minecraft:villager,tag=rpg.vacant,limit=1,sort=random] at @s run function rpg:vacant/creep
