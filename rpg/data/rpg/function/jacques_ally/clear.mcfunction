# 清掉所有友军雅克与他们的特效。
execute as @e[type=minecraft:iron_golem,tag=rpg.jqa] at @s run function rpg:jacques_ally/remove
kill @e[tag=rpg.jqa.fx]
