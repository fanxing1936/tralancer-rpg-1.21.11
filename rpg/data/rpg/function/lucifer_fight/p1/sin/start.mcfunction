execute if entity @s[tag=rpg.advent] at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_1
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m1
function rpg:lucifer_fight/p1/aim
scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
tag @s add rpg.lu1f.self
execute as @e[type=minecraft:marker,tag=rpg.lu1f.aim] if score @s rpg_l2_id = #id rpg_l2_id rotated as @s as @e[tag=rpg.lu1f.self,limit=1] at @s rotated ~ 0 run function rpg:lucifer_fight/p1/sin/warn
tag @s remove rpg.lu1f.self
