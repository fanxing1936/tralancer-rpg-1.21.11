execute if entity @s[tag=rpg.advent] at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_2
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m2
function rpg:lucifer_fight/p1/aim
execute positioned ^-0.4 ^2.1 ^0.9 run function rpg:lucifer_fight/p1/fx/glint
scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
tag @s add rpg.lu1f.self
execute as @e[type=minecraft:marker,tag=rpg.lu1f.aim] if score @s rpg_l2_id = #id rpg_l2_id rotated as @s as @e[tag=rpg.lu1f.self,limit=1] at @s rotated ~ 0 run function rpg:lucifer_fight/p1/spear/warn
tag @s remove rpg.lu1f.self
