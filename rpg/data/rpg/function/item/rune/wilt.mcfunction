# 枯萎［被动］—— 攻击时四分之一的概率让目标凋零。
# 走 rpg.hurt + on attacker，与包里其余被动同一形状。
execute if entity @e[tag=rpg.hurt] run function rpg:item/rune/wilt/g0
tag @a[tag=rpg.rune.wilt] remove rpg.rune.wilt
