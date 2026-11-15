execute if score @s rpg_jq_t matches 40 if entity @e[tag=rpg.jqb.stone] run return run function rpg:jacques_boss/david/hit
execute if score @s rpg_jq_t matches 2 as @e[tag=rpg.jqb.stone] run function rpg:jacques_boss/david/stone_up
execute if score @s rpg_jq_t matches 20 as @e[tag=rpg.jqb.stone] run function rpg:jacques_boss/david/stone_fall
execute if score @s rpg_jq_t matches 20 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=0}] at @s run function rpg:jacques_boss/stakes/light
execute if score @s rpg_jq_t matches 32 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=1}] at @s run function rpg:jacques_boss/stakes/light
execute if score @s rpg_jq_t matches 44 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=2}] at @s run function rpg:jacques_boss/stakes/light
execute if score @s rpg_jq_t matches 56 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=3}] at @s run function rpg:jacques_boss/stakes/light
execute if score @s rpg_jq_t matches 68 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=4}] at @s run function rpg:jacques_boss/stakes/light
execute if score @s rpg_jq_t matches 80 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=5}] at @s run function rpg:jacques_boss/stakes/light
execute if score @s rpg_jq_t matches 92 as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=6}] at @s run function rpg:jacques_boss/stakes/light
scoreboard players operation #m rpg_jq = @s rpg_jq_t
scoreboard players set #k rpg_jq 10
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 if score @s rpg_jq_t matches 20..110 as @e[type=minecraft:marker,tag=rpg.jqb.stake,tag=rpg.jqb.lit] at @s run function rpg:jacques_boss/stakes/wall
execute if score #m rpg_jq matches 0 if score @s rpg_jq_t matches 20..110 as @e[type=minecraft:marker,tag=rpg.jqb.stake,tag=rpg.jqb.lit] at @s run function rpg:jacques_boss/stakes/blaze
execute if score @s rpg_jq_t matches 110 run function rpg:jacques_boss/stakes/pull
execute if score @s rpg_jq_t matches 125 at @e[type=minecraft:marker,tag=rpg.jqb.stakec,limit=1] run function rpg:jacques_boss/stakes/close
execute if score @s rpg_jq_t matches 127.. run function rpg:jacques_boss/skill/stagger
