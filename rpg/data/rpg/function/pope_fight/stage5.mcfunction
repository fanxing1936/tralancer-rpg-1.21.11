# 末影之心倒下：死亡动作放完，外壳才碎。
execute if score #bl rpg_pf matches 1.. run function rpg:pope_fight/heart/blend_tick
execute if score #t rpg_pf matches 86 run function rpg:pope_fight/heart/shatter
execute if score #t rpg_pf matches 118.. run function rpg:pope_fight/victory
