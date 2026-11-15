scoreboard players operation #m rpg_jq = @s rpg_jq_t
scoreboard players set #k rpg_jq 8
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run function rpg:jacques_boss/stagger_star
execute if score @s rpg_jq_t matches 60.. run function rpg:jacques_boss/stagger/end
