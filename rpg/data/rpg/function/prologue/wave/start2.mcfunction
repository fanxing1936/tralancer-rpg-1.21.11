scoreboard players set #wave rpg_pr 2
scoreboard players set #wt rpg_pr 0
title @a[tag=rpg.pr] times 10 80 20
title @a[tag=rpg.pr] subtitle {"translate":"rpg.prologue.T03.en","fallback":"Wave 2 · Skills","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pr] title {"translate":"rpg.prologue.T03.zh","fallback":"第二波 · 技能","color":"#E8D9B0","bold":true}
function rpg:prologue/sub/t04
scoreboard players operation #k rpg_pr = #n rpg_pr
scoreboard players operation #k rpg_pr += #n rpg_pr
scoreboard players add #k rpg_pr 4
function rpg:prologue/wave/spawn
