# as/at 目标：#dmg = 伤害（十分之一点），#hm = 对恶魔与亡灵的倍率（十分之一）
scoreboard players operation #d rpg_fo = #dmg rpg_fo
function rpg:force/unholy
execute if score #u rpg_fo matches 1 run scoreboard players operation #d rpg_fo *= #hm rpg_fo
execute if score #u rpg_fo matches 1 run scoreboard players operation #d rpg_fo /= #10 rpg_fo
execute if entity @a[tag=rpg.fo.me,limit=1] run function rpg:force/x/id/spell_mod
execute if entity @s[tag=rpg.el.h] if score #tree rpg_fo matches 1 run scoreboard players operation #d rpg_fo /= #2 rpg_fo
execute if entity @s[tag=rpg.el.h] if score #tree rpg_fo matches 2 run scoreboard players operation #d rpg_fo *= #13 rpg_fo
execute if entity @s[tag=rpg.el.h] if score #tree rpg_fo matches 2 run scoreboard players operation #d rpg_fo /= #10 rpg_fo
execute store result storage rpg:force h.d float 0.1 run scoreboard players get #d rpg_fo
execute if entity @a[tag=rpg.fo.me,limit=1] run return run function rpg:force/hit_by with storage rpg:force h
function rpg:force/hit_no with storage rpg:force h
