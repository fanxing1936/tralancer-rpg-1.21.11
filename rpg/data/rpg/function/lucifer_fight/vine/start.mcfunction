execute if entity @s[tag=rpg.advent] at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_1
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m45
function rpg:lucifer_p2/play/jungleabomination_vineattack
scoreboard players set @s rpg_l2_v 0
scoreboard players set #hit rpg_l2_v 0
tag @e[tag=rpg.unit] remove rpg.lu2f.hit
execute as @e[tag=rpg.unit.f,distance=..16,limit=4,sort=nearest] at @s run function rpg:lucifer_fight/vine/mark_player
scoreboard players operation @e[tag=rpg.lu2f.new] rpg_l2_id = @s rpg_l2_id
scoreboard players set @e[tag=rpg.lu2f.new] rpg_l2_t 30
tag @e[tag=rpg.lu2f.new] remove rpg.lu2f.new
