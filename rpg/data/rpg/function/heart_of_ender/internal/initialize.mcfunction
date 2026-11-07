tag @s remove rpg.he.new
scoreboard players add #next rpg_he_id 1
scoreboard players operation @s rpg_he_id = #next rpg_he_id
scoreboard players operation #owner rpg_he_id = @s rpg_he_id
execute on passengers if entity @s[tag=rpg.he.part] run scoreboard players operation @s rpg_he_id = #owner rpg_he_id
function rpg:heart_of_ender/anim/enter/idle
