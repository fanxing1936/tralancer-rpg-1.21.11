execute if score @s rpg_l2_t matches 4 as @e[tag=rpg.unit.f,distance=..24,sort=nearest,limit=4] at @s run function rpg:lucifer_boss/fs/star/mark
execute if score @s rpg_l2_t matches 14 as @e[type=minecraft:marker,tag=rpg.lub.star] at @s run function rpg:lucifer_boss/fs/star/fall
execute if score @s rpg_l2_t matches 34 as @e[type=minecraft:marker,tag=rpg.lub.star] at @s run function rpg:lucifer_boss/fs/star/hit
execute if score @s rpg_l2_t matches 52.. run function rpg:lucifer_fight/free
