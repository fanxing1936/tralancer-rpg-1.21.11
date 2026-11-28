scoreboard players set #cd rpg_pr_i1 1
function rpg:prologue_i1/lobby/fix_lucifer
execute if score #n rpg_pr_i1 matches ..3 run function rpg:prologue_i1/sub/u08
execute if score #n rpg_pr_i1 matches 4.. run function rpg:prologue_i1/sub/u07
