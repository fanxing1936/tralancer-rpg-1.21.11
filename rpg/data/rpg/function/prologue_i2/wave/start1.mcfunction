scoreboard players set #wave rpg_pr_i2 1
scoreboard players set #wt rpg_pr_i2 0
title @a[tag=rpg.pri2] times 10 80 20
title @a[tag=rpg.pri2] subtitle {"translate":"rpg.prologue.T01.en","fallback":"Wave 1 · Movement and Attacks","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pri2] title {"translate":"rpg.prologue.T01.zh","fallback":"第一波 · 移动与普攻","color":"#E8D9B0","bold":true}
function rpg:prologue_i2/sub/t02
scoreboard players operation #k rpg_pr_i2 = #n rpg_pr_i2
scoreboard players operation #k rpg_pr_i2 += #n rpg_pr_i2
scoreboard players add #k rpg_pr_i2 4
function rpg:prologue_i2/wave/spawn
