# 序章结束、被中止、场地没备好或中途掉线后还原（接在每个战场的 iso/restore 末尾）：进正式游戏
tag @s remove rpg.ob.pro
tag @s remove rpg.ob.queued
tag @s remove rpg.pr.q
execute unless score @s rpg_ob matches 1 run return 0
tag @s add rpg.ob.fin
scoreboard players set @s rpg_ob_t 0
