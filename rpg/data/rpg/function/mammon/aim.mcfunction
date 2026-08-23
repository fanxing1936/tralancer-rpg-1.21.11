# 抖一下方向，接上归属与伤害。
#
# crit 与 PierceLevel 不能写在 summon 的 NBT 里：箭在构造时会自己重算这两项，
# 写进去的值当场就没了（实测 summon 给 5b，读回来是 0b）。落地之后再 data modify
# 就留得住 —— 所以这两行必须在这里，不能挪回上面那条 summon。
tag @s remove rpg.mam.new
data modify entity @s Owner set from storage rpg:mam owner
data modify entity @s damage set from storage rpg:mam dmg
data modify entity @s weapon set from storage rpg:mam weapon
data modify entity @s crit set value 1b
data modify entity @s PierceLevel set from storage rpg:mam pierce

execute store result score #jx rpg_mam run random value -250..250
execute store result score #jy rpg_mam run random value -110..110
execute store result score #jz rpg_mam run random value -250..250
scoreboard players operation #jx rpg_mam += #mx rpg_mam
scoreboard players operation #jy rpg_mam += #my rpg_mam
scoreboard players operation #jz rpg_mam += #mz rpg_mam
execute store result entity @s Motion[0] double 0.001 run scoreboard players get #jx rpg_mam
execute store result entity @s Motion[1] double 0.001 run scoreboard players get #jy rpg_mam
execute store result entity @s Motion[2] double 0.001 run scoreboard players get #jz rpg_mam
