execute if score @s rpg_jq_t matches 18 run function rpg:jacques/anim/enter/shoot
execute if score @s rpg_jq_t matches 18 run particle minecraft:end_rod ~ ~2.2 ~ 0.2 2 0.2 0.1 30
execute if score @s rpg_jq_t matches 18 run function rpg:jacques_boss/vfx/harp_sky
execute if score @s rpg_jq_t matches 2..17 run particle minecraft:enchant ~ ~1.6 ~ 1 1 1 1 8
execute if score @s rpg_jq_t matches 18 run playsound rpg:jacques.fire hostile @a[distance=..32] ~ ~ ~ 1.2 1
execute if score @s rpg_jq_t matches 30 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=0}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 35 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=1}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 40 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=2}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 45 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=3}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 50 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=4}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 55 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=5}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 60 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=6}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 65 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=7}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 70 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=8}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 75 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=9}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 80 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=10}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 85 as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=11}] at @s run function rpg:jacques_boss/harp/fall
execute if score @s rpg_jq_t matches 96.. run function rpg:jacques_boss/stagger/end
