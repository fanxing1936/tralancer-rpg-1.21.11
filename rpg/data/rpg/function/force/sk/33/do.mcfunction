scoreboard players add @s rpg_al_cd 0
scoreboard players operation #al rpg_fo = @s rpg_al_cd
function rpg:jacques_ally/summon
scoreboard players operation @s rpg_al_cd = #al rpg_fo
