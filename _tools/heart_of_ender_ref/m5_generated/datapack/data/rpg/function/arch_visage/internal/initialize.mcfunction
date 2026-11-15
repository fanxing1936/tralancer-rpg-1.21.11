tag @s remove rpg.av.new
scoreboard players add #next rpg_av_id 1
scoreboard players operation @s rpg_av_id = #next rpg_av_id
scoreboard players operation #owner rpg_av_id = @s rpg_av_id
execute on passengers if entity @s[tag=rpg.av.part] run scoreboard players operation @s rpg_av_id = #owner rpg_av_id
function rpg:arch_visage/anim/enter/spawn_attack
