scoreboard players operation #m rpg_lub = @s rpg_l2_t
scoreboard players set #k rpg_lub 2
scoreboard players operation #m rpg_lub %= #k rpg_lub
execute if score @s rpg_l2_t matches 8 as @e[tag=rpg.unit.f,distance=..20,sort=nearest,limit=4] run function rpg:lucifer_boss/fs/thorn/aim
execute if score @s rpg_l2_t matches 10..42 if score #m rpg_lub matches 0 as @e[type=minecraft:marker,tag=rpg.lub.thorn] at @s run function rpg:lucifer_boss/fs/thorn/step
execute if score @s rpg_l2_t matches 43 run kill @e[type=minecraft:marker,tag=rpg.lub.thorn]
execute if score @s rpg_l2_t matches 60.. run function rpg:lucifer_fight/free
