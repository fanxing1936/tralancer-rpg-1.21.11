# 序章结束、被中止或中途掉线后还原（接在 rpg:prologue/iso/restore 末尾）：进黑屏，下一步
tag @s remove rpg.ob.pro
tag @s remove rpg.ob.queued
execute unless score @s rpg_ob matches 1 run return 0
scoreboard players set @s rpg_ob 3
function rpg:onboard/hold/enter
tag @s add rpg.ob.wait
scoreboard players set @s rpg_ob_t 0
