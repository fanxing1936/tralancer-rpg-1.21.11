# 无处可去的东西不再散成碎片 —— 它随机招来一位领主作为躯体。
#
# 这条恶魔属于空缺者，不属于动手的人；玩家签了谁都不影响掷点。
# 仍复用降临的七柱分流，只是这一只是来打架的，所以寿命另算。
scoreboard players set #boss rpg_fall 1
execute store result score #lord rpg_fall run random value 1..7
execute at @s run function rpg:taint/lord
