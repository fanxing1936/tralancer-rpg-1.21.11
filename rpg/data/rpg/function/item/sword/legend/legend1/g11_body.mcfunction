# 由 opt_invert.py 内外翻：原本这 4 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run effect give @e[distance=0..2] minecraft:wind_charged 20 40 true
execute at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run particle dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:3} ~1 ~2 ~1 -2 -2 -2 1 50
execute at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run particle minecraft:gust_emitter_small ~0.5 ~1.2 ~0.5 -1 -1 -1 1 2
execute at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.8d,0d]}
