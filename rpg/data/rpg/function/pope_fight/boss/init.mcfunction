# 教皇：不走路，靠瞬移；不带 rpg.demon，所以上位契约打不到他。
data merge entity @s {NoAI:1b}
attribute @s minecraft:max_health base set 1000
attribute @s minecraft:armor base set 10
attribute @s minecraft:knockback_resistance base set 1
data merge entity @s {Health:1000.0f}
function rpg:pope_fight/clip/appear
