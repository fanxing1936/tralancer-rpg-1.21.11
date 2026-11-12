execute if entity @s[tag=rpg.advent] at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m45
function rpg:lucifer_p2/play/jungleabomination_vineattack
scoreboard players set @s rpg_l2_v 0
scoreboard players set #hit rpg_l2_v 0
tag @a remove rpg.lu2f.hit
execute as @a[distance=..16,gamemode=!spectator,gamemode=!creative,limit=4,sort=nearest] at @s run function rpg:lucifer_fight/vine/mark_player
scoreboard players operation @e[tag=rpg.lu2f.new] rpg_l2_id = @s rpg_l2_id
scoreboard players set @e[tag=rpg.lu2f.new] rpg_l2_t 30
tag @e[tag=rpg.lu2f.new] remove rpg.lu2f.new
