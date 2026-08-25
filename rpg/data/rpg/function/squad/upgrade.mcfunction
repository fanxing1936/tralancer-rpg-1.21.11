# 升级。潜行 + 募兵旗，对着身边的在编佣兵。
#
# 和掷点各有各的位置：掷点便宜但看运气，升级**确定**，所以按目标等级的
# **全价**收 —— 你买的是"这一次一定成"。
# 选择器不能直接比较实体与雇主的队伍编号，所以先把这一队的近身候选人挂上
# 只在本次同步调用里存活的 pick，然后再从中取最近的一个。不能先 limit=1
# 再验编号：另一个玩家的佣兵站得更近时，会把自己的人挡掉。
tag @s add rpg.sq.boss
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..6] if score @s rpg_squad = #sq rpg_squad run tag @s add rpg.sq.pick
execute unless entity @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..6] run function rpg:squad/none_near
scoreboard players set #tier rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..6,limit=1,sort=nearest] run scoreboard players operation #tier rpg_squad = @s rpg_sq_tier
execute if score #tier rpg_squad matches 5.. run function rpg:squad/up_max
execute store result score @s rpg_sq_have run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
execute if score #tier rpg_squad matches 1 run function rpg:squad/up2
execute if score #tier rpg_squad matches 2 run function rpg:squad/up3
execute if score #tier rpg_squad matches 3 run function rpg:squad/up4
execute if score #tier rpg_squad matches 4 run function rpg:squad/up5
tag @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..6] remove rpg.sq.pick
tag @s remove rpg.sq.boss
