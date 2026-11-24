scoreboard players set #cd rpg_pr 1
function rpg:prologue/lobby/fix_lucifer
execute if score #n rpg_pr matches ..3 run function rpg:prologue/sub/u08
execute if score #n rpg_pr matches 4.. run function rpg:prologue/sub/u07
