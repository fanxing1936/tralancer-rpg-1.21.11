# 都灵裹尸布（全金属盔甲胸甲）的穿戴外观：每个穿着它的玩家一个展示实体，
# 每刻跟到玩家脚下。没人穿、也没有残留时直接返回。
execute unless entity @a[predicate=rpg:full_metal/wearing,limit=1] unless entity @e[type=minecraft:item_display,tag=rpg.fm.part,limit=1] run return 0
tag @e[type=minecraft:item_display,tag=rpg.fm.part] remove rpg.fm.seen
execute as @a[predicate=rpg:full_metal/wearing,predicate=!rpg:full_metal/hidden,gamemode=!spectator] at @s run function rpg:full_metal/follow
# 脱下、隐身、下线、离得太远：没被认领的一律清掉
kill @e[type=minecraft:item_display,tag=rpg.fm.part,tag=!rpg.fm.seen]
