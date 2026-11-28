scoreboard players set #wave rpg_pr_i4 3
scoreboard players set #wt rpg_pr_i4 0
title @a[tag=rpg.pri4] times 10 80 20
title @a[tag=rpg.pri4] subtitle {"translate":"rpg.prologue.T05.en","fallback":"Wave 3 · The Throne","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pri4] title {"translate":"rpg.prologue.T05.zh","fallback":"第三波 · 座天使","color":"#E8D9B0","bold":true}
function rpg:prologue_i4/sub/t06
execute in rpg:armageddon_4 positioned 10 83 0 run function rpg:prologue_i4/throne/summon
