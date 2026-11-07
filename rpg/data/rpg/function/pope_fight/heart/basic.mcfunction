# 普攻（爬行途中）：近了咬，远了吐。不打断下一招的计时。
scoreboard players set #ba rpg_pf 0
execute if entity @a[tag=rpg.pf.tgt,limit=1,distance=..8] run return run function rpg:pope_fight/heart/start_bite
execute if entity @a[tag=rpg.pf.tgt,limit=1,distance=..26] run function rpg:pope_fight/heart/start_spit
