scoreboard players set #wave rpg_pr_i3 3
scoreboard players set #wt rpg_pr_i3 0
title @a[tag=rpg.pri3] times 10 80 20
title @a[tag=rpg.pri3] subtitle {"translate":"rpg.prologue.T05.en","fallback":"Wave 3 · The Throne","color":"#BFB8A8","italic":true}
title @a[tag=rpg.pri3] title {"translate":"rpg.prologue.T05.zh","fallback":"第三波 · 座天使","color":"#E8D9B0","bold":true}
function rpg:prologue_i3/sub/t06
execute in rpg:armageddon_3 positioned 10 83 0 run function rpg:prologue_i3/throne/summon
