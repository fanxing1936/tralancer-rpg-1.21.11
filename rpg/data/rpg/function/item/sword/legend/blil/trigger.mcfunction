# 贝利尔 · 朝拜：瞬发，但长按不会每刻重复结算。
advancement revoke @s only rpg:item/blil
execute if entity @s[tag=rpg.h.blil_tag1,scores={rpg_blil_cd=..0}] run function rpg:item/legacy/blil_cast
