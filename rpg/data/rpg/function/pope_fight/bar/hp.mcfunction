# #hp 换算成档位，变了才换图。
scoreboard players operation #hud rpg_pf = #hp rpg_pf
scoreboard players operation #hud rpg_pf /= #fifty rpg_pf
execute if score #hud rpg_pf matches 0 if score #hp rpg_pf matches 1.. run scoreboard players set #hud rpg_pf 1
execute unless score #hud rpg_pf = #hudl rpg_pf run function rpg:pope_fight/bar/show
