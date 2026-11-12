execute if score @s rpg_l2_t matches 12 run function rpg:lucifer_lord/play/strong
execute if score @s rpg_l2_t matches 12 run scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
execute if score @s rpg_l2_t matches 12 run tag @s add rpg.lu1f.self
execute if score @s rpg_l2_t matches 12 run execute as @e[type=minecraft:marker,tag=rpg.lu1f.aim] if score @s rpg_l2_id = #id rpg_l2_id rotated as @s as @e[tag=rpg.lu1f.self,limit=1] at @s rotated ~ 0 run function rpg:lucifer_fight/p1/sin/fire
execute if score @s rpg_l2_t matches 12 run tag @s remove rpg.lu1f.self
execute if score @s rpg_l2_t matches 32 run function rpg:lucifer_fight/free
