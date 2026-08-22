# 由 opt_invert.py 内外翻：原本这 18 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] store result score @s random run random value 1..5
execute at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run effect give @e[limit=1,sort=nearest] wither 5 10 true
execute at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":5,"Fuse":0}
execute at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run effect give @s resistance 5 10 false
execute at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run particle gust_emitter_small ~0.5 ~1.5 ~0.5 -1 -1 -1 1 10
execute at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run function rpg:item/sword/legend/wukong/particle
execute at @s on attacker if entity @s[scores={wukong=0..,random=2},tag=rpg.h.wukong_tag1] run effect give @s minecraft:instant_health 1 1 true
execute at @s on attacker if entity @s[scores={wukong=0..,random=2},tag=rpg.h.wukong_tag1] run particle minecraft:totem_of_undying ~1 ~1.5 ~1 -2 -2 -2 1 50
execute at @s on attacker if entity @s[scores={wukong=0..,random=2},tag=rpg.h.wukong_tag1] run playsound minecraft:item.mace.smash_ground_heavy
execute at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run effect give @e[distance=0..1] minecraft:slowness 3 255 true
execute at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run particle enchant ~1 ~1.5 ~1 -2 -2 -2 1 50
execute at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run effect give @e[distance=0..1] minecraft:glowing 3 255 true
execute at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run playsound minecraft:item.mace.smash_ground_heavy
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run effect give @e[distance=0..2] minecraft:wind_charged 10 10 true
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run particle dust_color_transition{from_color:[1.0,0.35,0.0],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run particle dust_color_transition{from_color:[1.0,0.87,0.0],to_color:[1.0,1.0,1.0],scale:2} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
