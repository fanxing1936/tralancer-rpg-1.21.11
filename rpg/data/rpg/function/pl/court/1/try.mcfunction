# 有人走近（at 中心）：过了前一座的人在场才开
execute unless entity @a[distance=..12,gamemode=!spectator] run return 0
scoreboard players set #l1 rpg_pl 1
scoreboard players set #f1 rpg_pl 0
function rpg:pl/court/1/layer
