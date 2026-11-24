execute unless score #do rpg_ob matches 3..4 run return 0
scoreboard players operation #do rpg_fg = #do rpg_ob
function rpg:forge/wb/new
function rpg:forge/wb/load_off
function rpg:forge/op/wash/do
function rpg:forge/wb/save_off
function rpg:forge/wb/close
scoreboard players set @s rpg_ob 10
function rpg:onboard/show
