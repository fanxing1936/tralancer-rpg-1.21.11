scoreboard players add @s rpg_jq_n 1
execute facing entity @e[tag=rpg.unit.f,distance=..5.5,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_cb matches 0 run function rpg:jacques_boss/skill/slash1
execute if score @s rpg_jq_cb matches 1 run function rpg:jacques_boss/skill/slash2
execute if score @s rpg_jq_cb matches 2 run function rpg:jacques_boss/skill/sweep
scoreboard players add @s rpg_jq_cb 1
execute if score @s rpg_jq_cb matches 3.. run scoreboard players set @s rpg_jq_cb 0
