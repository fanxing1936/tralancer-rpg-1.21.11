scoreboard players operation #hudl rpg_pf = #hud rpg_pf
execute if score #stage rpg_pf matches ..3 run return run function rpg:pope_fight/bar/pope
execute if score #weak rpg_pf matches 1 run return run function rpg:pope_fight/bar/weak
function rpg:pope_fight/bar/heart
