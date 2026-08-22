# 8 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] store result score @s random run random value 1..5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d,0d]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] run particle gust ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.7 ~0.1 -0.2 -0.5 -0.2 0.1 5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.9,0.63,0.0],to_color:[0.15,0.91,0.76],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 2
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack by @s
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
