# 清除最终 Boss 的全部实体。模型部件随载体一起清掉；特效按寿命、罪仆按主人自行消失。
execute as @e[type=minecraft:vindicator,tag=rpg.lub] run function rpg:lucifer_boss/clear_unit
# 「蛇之后裔」召来的罪仆可以独立存活，这里一并带走
execute as @e[tag=rpg.lub.unit] run function rpg:lucifer_boss/clear_unit
kill @e[tag=rpg.lub.sword]
kill @e[type=minecraft:marker,tag=rpg.lub.star]
kill @e[type=minecraft:marker,tag=rpg.lub.thorn]
kill @e[type=minecraft:marker,tag=rpg.lub.center]
bossbar set rpg:lucifer_boss visible false
bossbar set rpg:lucifer_boss players
stopsound @a record minecraft:boss1
stopsound @a record minecraft:boss2
scoreboard players set #fight rpg_lub 0
scoreboard players set #stage rpg_lub 0
