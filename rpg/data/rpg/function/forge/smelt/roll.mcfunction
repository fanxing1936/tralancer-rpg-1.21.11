execute if score #souls rpg_fg matches ..0 run return 0
execute store result score #r rpg_fg run random value -10..15
execute if score #r rpg_fg > #best rpg_fg run scoreboard players operation #best rpg_fg = #r rpg_fg
scoreboard players remove #souls rpg_fg 1
function rpg:forge/smelt/roll
