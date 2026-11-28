# 只观察原版 AI 的攻击。用目标的受击时间和最近攻击者确认命中归属。
tag @s add rpg.tw.model.probing
execute on target if predicate rpg:town_models/just_hurt on attacker if entity @s[tag=rpg.tw.model.probing] at @s run function rpg:town_models/town_hollow/anim/enter/attack
tag @s remove rpg.tw.model.probing
