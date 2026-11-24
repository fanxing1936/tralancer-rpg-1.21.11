scoreboard players set #wave rpg_pr 3
scoreboard players set #wt rpg_pr 0
title @a[tag=rpg.pr] times 10 80 20
title @a[tag=rpg.pr] subtitle {"translate":"rpg.prologue.T05.en","fallback":"Wave 3 · The Throne","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pr] title {"translate":"rpg.prologue.T05.zh","fallback":"第三波 · 座天使","color":"#E8D9B0","bold":true}
function rpg:prologue/sub/t06
execute in rpg:armageddon positioned 10 83 0 run function rpg:prologue/throne/summon
