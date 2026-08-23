# 驱魔仪式 —— 由 rpg:item/rite 在「以圣水右击灵魂灯笼」时触发。
# 阵型：以被点的灵魂灯笼为心，四正方向各三格处再各有一盏。
advancement revoke @s only rpg:item/rite
execute if entity @s[scores={rpg_rite=1..}] run return 0
execute at @s run function rpg:rite/check
