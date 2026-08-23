# 临界 —— 攻击 +10
attribute @s minecraft:attack_damage modifier add rpg:fall 10 add_value
execute at @s run particle dust{color:[0.38,0.0,0.04],scale:2.6} ~ ~1 ~ 0.4 0.7 0.4 0.02 20
effect give @s minecraft:nausea 6 0 true
execute if predicate rpg:fall4 run function rpg:taint/yank_roll
# 脚步忽快忽慢 —— 不是你在走
execute if predicate rpg:fall4 run effect give @s minecraft:slowness 2 1 true
execute unless predicate rpg:fall4 run effect give @s minecraft:speed 2 1 true
execute if predicate rpg:fall4 run effect give @s minecraft:darkness 3 0 true
playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1 0.6
# 最深一档：手自己动起来
execute if predicate rpg:fall4 run function rpg:taint/swing_roll
