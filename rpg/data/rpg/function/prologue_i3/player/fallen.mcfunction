execute unless entity @s[tag=rpg.pri3] run return run advancement revoke @s only rpg:prologue_i3/fallen
advancement revoke @s only rpg:prologue_i3/fallen
execute unless entity @s[tag=rpg.pri3] run return 0
gamemode spectator @s
scoreboard players set @s rpg_pr_down 100
title @s times 5 70 10
title @s subtitle {"translate":"rpg.prologue.T10.en","fallback":"You have fallen. Rejoining at the edge of the field in 5 seconds","color":"#BFB8A8"}
title @s title {"translate":"rpg.prologue.T10.zh","fallback":"你倒下了，5 秒后在战场边缘重新加入","color":"#E8D9B0"}
