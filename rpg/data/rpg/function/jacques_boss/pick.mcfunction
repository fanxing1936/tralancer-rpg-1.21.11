scoreboard players set @s rpg_jq_n 0
scoreboard players set #ult rpg_jq 0
execute if score @s rpg_jq matches 1 if score @s rpg_jq_h matches ..625 unless entity @s[tag=rpg.jqb.u1] run scoreboard players set #ult rpg_jq 1
execute if score @s rpg_jq matches 1 if score @s rpg_jq_h matches ..375 unless entity @s[tag=rpg.jqb.u2] run scoreboard players set #ult rpg_jq 2
execute if score @s rpg_jq matches 1 if score #ult rpg_jq matches 0 if score @s rpg_jq_c matches 900.. run scoreboard players set #ult rpg_jq 9
execute if score @s rpg_jq matches 2 if score @s rpg_jq_h matches ..667 unless entity @s[tag=rpg.jqb.u1] run scoreboard players set #ult rpg_jq 1
execute if score @s rpg_jq matches 2 if score @s rpg_jq_h matches ..333 unless entity @s[tag=rpg.jqb.u2] run scoreboard players set #ult rpg_jq 2
execute if score @s rpg_jq matches 2 if score #ult rpg_jq matches 0 if score @s rpg_jq_c matches 1200.. run scoreboard players set #ult rpg_jq 9
execute if score #ult rpg_jq matches 1.. run return run function rpg:jacques_boss/ult/pick
execute if score @s rpg_jq matches 1 run scoreboard players operation #r rpg_jq = @s rpg_jq_k
execute if score @s rpg_jq matches 1 if score #r rpg_jq matches 0 run function rpg:jacques_boss/pick/volley
execute if score @s rpg_jq matches 1 if score #r rpg_jq matches 1 run function rpg:jacques_boss/pick/charge
execute if score @s rpg_jq matches 1 if score #r rpg_jq matches 2 run function rpg:jacques_boss/pick/horn
execute if score @s rpg_jq matches 1 run scoreboard players add @s rpg_jq_k 1
execute if score @s rpg_jq matches 1 if score @s rpg_jq_k matches 3.. run scoreboard players set @s rpg_jq_k 0
execute if score @s rpg_jq matches 2 run scoreboard players operation #r rpg_jq = @s rpg_jq_k
execute if score @s rpg_jq matches 2 if score #r rpg_jq matches 0 run function rpg:jacques_boss/pick/leap
execute if score @s rpg_jq matches 2 if score #r rpg_jq matches 1 run function rpg:jacques_boss/pick/volley
execute if score @s rpg_jq matches 2 if score #r rpg_jq matches 2 run function rpg:jacques_boss/pick/curse
execute if score @s rpg_jq matches 2 if score #r rpg_jq matches 3 run function rpg:jacques_boss/pick/horn
execute if score @s rpg_jq matches 2 run scoreboard players add @s rpg_jq_k 1
execute if score @s rpg_jq matches 2 if score @s rpg_jq_k matches 4.. run scoreboard players set @s rpg_jq_k 0
