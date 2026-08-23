# 夺舍 —— 攻击 +6
attribute @s minecraft:attack_damage modifier add rpg:fall 6 add_value
execute at @s run particle dust{color:[0.62,0.09,0.12],scale:2.2} ~ ~1 ~ 0.4 0.7 0.4 0.02 16
effect give @s minecraft:nausea 5 0 true
execute if predicate rpg:fall3 run function rpg:taint/yank_roll
# 脚步忽快忽慢 —— 不是你在走
execute if predicate rpg:fall3 run effect give @s minecraft:slowness 2 1 true
execute unless predicate rpg:fall3 run effect give @s minecraft:speed 2 1 true
playsound minecraft:entity.wither.ambient master @s ~ ~ ~ 0.5 0.5
