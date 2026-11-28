scoreboard players set #cd rpg_pr_i2 1
function rpg:prologue_i2/lobby/fix_lucifer
execute if score #n rpg_pr_i2 matches ..3 run function rpg:prologue_i2/sub/u08
execute if score #n rpg_pr_i2 matches 4.. run function rpg:prologue_i2/sub/u07
