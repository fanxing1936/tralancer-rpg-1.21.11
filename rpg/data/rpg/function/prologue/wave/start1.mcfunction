scoreboard players set #wave rpg_pr 1
scoreboard players set #wt rpg_pr 0
title @a[tag=rpg.pr] times 10 80 20
title @a[tag=rpg.pr] subtitle {"translate":"rpg.prologue.T01.en","fallback":"Wave 1 · Movement and Attacks","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pr] title {"translate":"rpg.prologue.T01.zh","fallback":"第一波 · 移动与普攻","color":"#E8D9B0","bold":true}
function rpg:prologue/sub/t02
scoreboard players operation #k rpg_pr = #n rpg_pr
scoreboard players operation #k rpg_pr += #n rpg_pr
scoreboard players add #k rpg_pr 4
function rpg:prologue/wave/spawn
