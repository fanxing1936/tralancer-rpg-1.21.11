# 有人走近（at 中心）：过了前一座的人在场才开
execute unless entity @a[distance=..12,gamemode=!spectator,scores={rpg_pl_best=15..}] run return run title @a[distance=..12] actionbar ["",{"text":"先过前一座河庭","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set #l4 rpg_pl 1
scoreboard players set #f4 rpg_pl 0
function rpg:pl/court/4/layer
