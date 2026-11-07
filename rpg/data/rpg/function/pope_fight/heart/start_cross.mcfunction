scoreboard players set #sk rpg_pf 3
scoreboard players set #st rpg_pf 0
scoreboard players set #walking rpg_pf 0
function rpg:pope_fight/heart/clip/cross_beam
# 光束每次换方向，起手角也错开 45 度。
scoreboard players add #dir rpg_pf 1
execute if score #dir rpg_pf matches 2.. run scoreboard players set #dir rpg_pf 0
function rpg:pope_fight/heart/weak_on
