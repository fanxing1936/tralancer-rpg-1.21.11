scoreboard players set @s rpg_l2_st 3
scoreboard players set @s rpg_l2_t 0
scoreboard players operation @s rpg_l2_sk = #pick rpg_l2_v
scoreboard players add @s rpg_l2_sk 10
function rpg:lucifer_fight/hold
