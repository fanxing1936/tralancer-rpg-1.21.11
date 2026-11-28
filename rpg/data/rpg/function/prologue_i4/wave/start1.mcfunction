scoreboard players set #wave rpg_pr_i4 1
scoreboard players set #wt rpg_pr_i4 0
title @a[tag=rpg.pri4] times 10 80 20
title @a[tag=rpg.pri4] subtitle {"translate":"rpg.prologue.T01.en","fallback":"Wave 1 · Movement and Attacks","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pri4] title {"translate":"rpg.prologue.T01.zh","fallback":"第一波 · 移动与普攻","color":"#E8D9B0","bold":true}
function rpg:prologue_i4/sub/t02
scoreboard players operation #k rpg_pr_i4 = #n rpg_pr_i4
scoreboard players operation #k rpg_pr_i4 += #n rpg_pr_i4
scoreboard players add #k rpg_pr_i4 4
function rpg:prologue_i4/wave/spawn
