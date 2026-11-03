# 第一下打在盾上：盾碎，部件移除（只是外观，血量照常扣）。
tag @s add rpg.vg.broken
execute on passengers if entity @s[tag=rpg.vg.p.shield] run kill @s
execute at @s run particle block{block_state:"minecraft:spruce_planks"} ~ ~1.2 ~ 0.4 0.5 0.4 0.1 24
function rpg:vanguard/anim/enter/break
