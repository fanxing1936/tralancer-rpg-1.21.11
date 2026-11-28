# 镇内不刷敌对怪：外来的普通怪直接送走（副本的怪、骑着模型的首领、友军不动）
execute if entity @s[tag=rpg.tw.lm] run return 0
tp @e[type=#rpg:elite_pool,distance=..72,tag=!rpg.tw.ev,tag=!rpg.ally,predicate=!rpg:town/ridden] ~ -400 ~
