# 每刻最多给 4 只新生物配装。
# 一次性召唤一群时，如果不封顶，全部的战利品表掷点会挤在同一刻。
tag @e[type=minecraft:creeper,tag=!creeper,limit=4] add rpg.spawn.new
execute as @e[tag=rpg.spawn.new] at @s run function rpg:command/spawn/creeper
tag @e[tag=rpg.spawn.new] add creeper
tag @e[tag=rpg.spawn.new] remove rpg.spawn.new
