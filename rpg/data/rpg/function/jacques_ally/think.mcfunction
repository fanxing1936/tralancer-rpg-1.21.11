# 正在出招：走时间线，不动。
execute if score @s rpg_al_sk matches 1.. run return run function rpg:jacques_ally/move
scoreboard players remove @s rpg_al_b 1
# 目标：最近的敌人（20 格内，含隐身的 Boss 载体）
tag @e[tag=rpg.al.aim] remove rpg.al.aim
execute as @e[type=#rpg:seal_hostile,type=!minecraft:creeper,tag=!rpg.ally,tag=!rpg.jqd,tag=!rpg.jqb.preview,nbt=!{Invulnerable:1b},distance=..20,sort=nearest,limit=1] run tag @s add rpg.al.aim
execute unless entity @e[tag=rpg.al.aim,limit=1] run return run function rpg:jacques_ally/follow
execute if score @s rpg_al_b matches ..0 if entity @e[tag=rpg.al.aim,distance=..3.2] run return run function rpg:jacques_ally/melee
execute if score @s rpg_al_b matches ..0 if entity @e[tag=rpg.al.aim,distance=6..22] if predicate rpg:jacques_ally/shoot_roll run return run function rpg:jacques_ally/shot
execute unless entity @e[tag=rpg.al.aim,distance=..2.6] facing entity @e[tag=rpg.al.aim,limit=1] feet rotated ~ 0 run function rpg:jacques_ally/step
execute if entity @e[tag=rpg.al.aim,distance=..2.6] facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0
