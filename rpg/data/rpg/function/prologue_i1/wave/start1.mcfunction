scoreboard players set #wave rpg_pr_i1 1
scoreboard players set #wt rpg_pr_i1 0
title @a[tag=rpg.pri1] times 10 80 20
title @a[tag=rpg.pri1] subtitle {"translate":"rpg.prologue.T01.en","fallback":"Wave 1 · Movement and Attacks","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pri1] title {"translate":"rpg.prologue.T01.zh","fallback":"第一波 · 移动与普攻","color":"#E8D9B0","bold":true}
function rpg:prologue_i1/sub/t02
scoreboard players operation #k rpg_pr_i1 = #n rpg_pr_i1
scoreboard players operation #k rpg_pr_i1 += #n rpg_pr_i1
scoreboard players add #k rpg_pr_i1 4
function rpg:prologue_i1/wave/spawn
