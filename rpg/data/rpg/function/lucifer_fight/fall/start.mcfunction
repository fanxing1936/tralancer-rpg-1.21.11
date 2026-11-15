execute if entity @s[tag=rpg.advent] at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_4
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m48
scoreboard players set @s rpg_l2_v 0
execute at @e[tag=rpg.unit.f,distance=..20,limit=1,sort=nearest] run summon minecraft:marker ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.mark","rpg.lu2f.lmark","rpg.lu2f.new"]}
scoreboard players operation @e[tag=rpg.lu2f.new] rpg_l2_id = @s rpg_l2_id
scoreboard players set @e[tag=rpg.lu2f.new] rpg_l2_t 90
tag @e[tag=rpg.lu2f.new] remove rpg.lu2f.new
execute at @e[tag=rpg.unit.f,distance=..20,limit=1,sort=nearest] run function rpg:lucifer_fight/fall/mark_fx
function rpg:lucifer_p2/play/jungleabomination_fall
