scoreboard players set #cd rpg_pr_i4 1
function rpg:prologue_i4/lobby/fix_lucifer
execute if score #n rpg_pr_i4 matches ..3 run function rpg:prologue_i4/sub/u08
execute if score #n rpg_pr_i4 matches 4.. run function rpg:prologue_i4/sub/u07
