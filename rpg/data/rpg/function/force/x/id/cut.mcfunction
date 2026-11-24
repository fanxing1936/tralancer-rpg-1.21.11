# 恶魔附近：新上身的负面效果时长 −30%（美丽阶起 −60%），每个效果只砍一次
data modify storage rpg:force r.l set from entity @s active_effects
function rpg:force/x/id/cut_loop
execute unless entity @s[tag=rpg.fo.p_poison] run tag @s remove rpg.fo.r_poison
execute unless entity @s[tag=rpg.fo.p_wither] run tag @s remove rpg.fo.r_wither
execute unless entity @s[tag=rpg.fo.p_slowness] run tag @s remove rpg.fo.r_slowness
execute unless entity @s[tag=rpg.fo.p_weakness] run tag @s remove rpg.fo.r_weakness
execute unless entity @s[tag=rpg.fo.p_blindness] run tag @s remove rpg.fo.r_blindness
execute unless entity @s[tag=rpg.fo.p_nausea] run tag @s remove rpg.fo.r_nausea
execute unless entity @s[tag=rpg.fo.p_hunger] run tag @s remove rpg.fo.r_hunger
execute unless entity @s[tag=rpg.fo.p_mining_fatigue] run tag @s remove rpg.fo.r_mining_fatigue
execute unless entity @s[tag=rpg.fo.p_darkness] run tag @s remove rpg.fo.r_darkness
execute unless entity @s[tag=rpg.fo.p_levitation] run tag @s remove rpg.fo.r_levitation
tag @s remove rpg.fo.p_poison
tag @s remove rpg.fo.p_wither
tag @s remove rpg.fo.p_slowness
tag @s remove rpg.fo.p_weakness
tag @s remove rpg.fo.p_blindness
tag @s remove rpg.fo.p_nausea
tag @s remove rpg.fo.p_hunger
tag @s remove rpg.fo.p_mining_fatigue
tag @s remove rpg.fo.p_darkness
tag @s remove rpg.fo.p_levitation
