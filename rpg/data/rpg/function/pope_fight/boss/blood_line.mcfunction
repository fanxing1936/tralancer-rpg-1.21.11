# 光线从杖头连到祭品：量出距离，再把展示实体拉到这么长。
scoreboard players set #d rpg_pf 0
execute positioned ^0.43 ^2.90 ^0.57 facing entity @e[type=minecraft:vindicator,tag=rpg.pf.sac,limit=1] eyes run function rpg:pope_fight/boss/blood_step
execute positioned ^0.43 ^2.90 ^0.57 facing entity @e[type=minecraft:vindicator,tag=rpg.pf.sac,limit=1] eyes run function rpg:pope_fight/boss/blood_aim
