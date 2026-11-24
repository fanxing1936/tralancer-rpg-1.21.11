execute unless entity @a[tag=rpg.fo.me,limit=1,scores={rpg_sef=5..}] run scoreboard players operation #d rpg_fo *= #125 rpg_fo
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_sef=5..}] run scoreboard players operation #d rpg_fo *= #150 rpg_fo
scoreboard players operation #d rpg_fo /= #100 rpg_fo
