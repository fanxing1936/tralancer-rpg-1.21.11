# 侵蚀 —— 攻击 +3
attribute @s minecraft:attack_damage modifier add rpg:fall 3 add_value
execute at @s run particle dust{color:[0.32,0.10,0.42],scale:1.8} ~ ~1 ~ 0.4 0.7 0.4 0.02 12
effect give @s minecraft:nausea 4 0 true
execute if predicate rpg:fall2 run function rpg:taint/yank_roll
playsound minecraft:entity.wither.ambient master @s ~ ~ ~ 0.4 0.5
