# 每刻最多给 4 只新生物配装。
# 一次性召唤一群时，如果不封顶，全部的战利品表掷点会挤在同一刻。
tag @e[type=#minecraft:skeletons,tag=!skeleton,limit=4] add rpg.spawn.new
execute as @e[tag=rpg.spawn.new] at @s run function rpg:command/spawn/skeleton
execute as @e[tag=rpg.spawn.new] run function rpg:command/spawn/skeleton_gear
tag @e[tag=rpg.spawn.new] add skeleton
tag @e[tag=rpg.spawn.new] remove rpg.spawn.new
