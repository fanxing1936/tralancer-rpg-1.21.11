# 清除最终 Boss 的全部实体。模型部件随载体一起清掉；特效按寿命、罪仆按主人自行消失。
execute as @e[type=minecraft:vindicator,tag=rpg.lub] run function rpg:lucifer_boss/clear_unit
kill @e[type=minecraft:marker,tag=rpg.lub.center]
bossbar set rpg:lucifer_boss visible false
bossbar set rpg:lucifer_boss players
stopsound @a record minecraft:boss1
stopsound @a record minecraft:boss2
scoreboard players set #fight rpg_lub 0
scoreboard players set #stage rpg_lub 0
