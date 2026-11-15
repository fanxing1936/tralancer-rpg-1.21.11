execute unless entity @e[tag=rpg.unit.f,distance=..25] run return 0
scoreboard players remove @s rpg_jq_b 1
execute if score @s rpg_jq_b matches 1.. run return 0
scoreboard players set @s rpg_jq_b 10
execute if score @s rpg_jq_n matches 3.. run return run function rpg:jacques_boss/pick
execute if entity @e[tag=rpg.unit.f,distance=..4.5] run return run function rpg:jacques_boss/basic/melee
execute unless entity @e[tag=rpg.unit.f,distance=..7] run return run function rpg:jacques_boss/basic/shot
# 4.5～7 格：不出手，走近
