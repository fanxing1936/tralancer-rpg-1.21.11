# 5 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] as @e[distance=0.1..2] at @s run damage @s 2 minecraft:player_attack
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run effect give @e[distance=0..2] glowing 5 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[1.0,1.0,1.0],scale:3} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 0.1 20
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
