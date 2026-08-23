# 每刻最多给 4 只新生物配装。
# 一次性召唤一群时，如果不封顶，全部的战利品表掷点会挤在同一刻。
# tag=!rpg.squad：佣兵也是尸壳，但他们是雇来的，不该被当作
# 新出生的野怪重掷装备、更不该被替换成强化变种。
tag @e[type=#minecraft:zombies,tag=!zombie,tag=!rpg.squad,limit=4] add rpg.spawn.new
execute as @e[tag=rpg.spawn.new] at @s run function rpg:command/spawn/zombie
execute as @e[tag=rpg.spawn.new] run function rpg:command/spawn/zombie_gear
tag @e[tag=rpg.spawn.new] add zombie
tag @e[tag=rpg.spawn.new] remove rpg.spawn.new
