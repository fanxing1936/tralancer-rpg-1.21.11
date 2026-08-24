# 由 opt_invert.py 内外翻：原本这 24 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] store result score @s random run random value 1..10
execute at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run effect give @e[limit=1,sort=nearest] wither 10 40 true
execute at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run summon minecraft:tnt ~ ~ ~ {fuse:0s,explosion_power:2.0f}
execute at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/flame
execute at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run effect give @s resistance 5 10 false
execute at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:1} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run effect give @e[limit=1,sort=nearest] minecraft:wither 20 40 true
execute at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run particle minecraft:soul_fire_flame ~1 ~1.5 ~1 -2 -2 -2 0.5 100
execute at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/particle
execute at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run effect give @s resistance 1 10 false
execute at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run playsound minecraft:item.mace.smash_ground_heavy
execute at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run effect give @e[distance=0..1] minecraft:slowness 5 255 true
execute at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run particle wax_off ~1 ~1.5 ~1 -2 -2 -2 1 100
execute at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/spark
execute at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run effect give @e[distance=0..1] minecraft:glowing 5 255 true
execute at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run effect give @s resistance 1 10 false
execute at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run playsound minecraft:item.mace.smash_ground_heavy
execute at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] at @e[limit=1,sort=nearest] run summon lightning_bolt
execute at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] run particle minecraft:soul ~1 ~1.5 ~1 -2 -2 -2 0.5 100
execute at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] run effect give @s resistance 1 10 false
execute at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/sweep
execute at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run effect give @e[distance=0..2,limit=1,sort=nearest] minecraft:weakness 10 5 true
execute at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[0.0,0.98,1.0],scale:2} ~0.5 ~1 ~0.5 -1 -1 -1 1 20
execute at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:2} ~0.5 ~1 ~0.5 -1 -1 -1 1 20
