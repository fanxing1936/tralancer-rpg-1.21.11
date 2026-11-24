function rpg:events/end
scoreboard players operation #now rpg_ev = #now rpg_ev
execute store result score #now rpg_ev run time query gametime
function rpg:events/e4/start
