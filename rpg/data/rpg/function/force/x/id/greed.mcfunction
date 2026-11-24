# 贪婪：残魂与器胚掉率 +50%（美丽阶起 +100%）——每次击杀按原掉率的一半再掷一次
execute store result score #r rpg_fo run random value 1..1000
execute if score #r rpg_fo matches ..25 run loot give @s loot rpg:forge/item/soul
execute if score @s rpg_sef matches 5.. if score #r rpg_fo matches 26..50 run loot give @s loot rpg:forge/item/soul
execute if score #r rpg_fo matches 501..505 run loot give @s loot rpg:forge/item/blank
execute if score @s rpg_sef matches 5.. if score #r rpg_fo matches 506..510 run loot give @s loot rpg:forge/item/blank
