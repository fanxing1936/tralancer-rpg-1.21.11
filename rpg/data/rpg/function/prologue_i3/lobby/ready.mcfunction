scoreboard players set #cd rpg_pr_i3 1
function rpg:prologue_i3/lobby/fix_lucifer
execute if score #n rpg_pr_i3 matches ..3 run function rpg:prologue_i3/sub/u08
execute if score #n rpg_pr_i3 matches 4.. run function rpg:prologue_i3/sub/u07
