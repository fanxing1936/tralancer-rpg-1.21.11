# 躁动 —— 攻击 +1
attribute @s minecraft:attack_damage modifier add rpg:fall 1 add_value
execute at @s run particle dust{color:[0.45,0.45,0.48],scale:1.4} ~ ~1 ~ 0.4 0.7 0.4 0.02 8
playsound minecraft:entity.wither.ambient master @s ~ ~ ~ 0.3 0.5
