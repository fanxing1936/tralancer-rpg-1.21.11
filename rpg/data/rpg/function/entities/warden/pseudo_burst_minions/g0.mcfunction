# 3 行原本各自扫一遍全实体表找 @e[type=minecraft:vindicator,tag=devil2,tag=tick]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:vindicator,tag=devil2,tag=tick] if score @s rpg_boom_id = @e[tag=rpg.pseudo_boom.source,limit=1] rpg_boom_id at @s run function rpg:effect/pseudo_explosion/sourced_p4
execute as @e[type=minecraft:vindicator,tag=devil2,tag=tick] if score @s rpg_boom_id = @e[tag=rpg.pseudo_boom.source,limit=1] rpg_boom_id at @s run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 100
execute as @e[type=minecraft:vindicator,tag=devil2,tag=tick] if score @s rpg_boom_id = @e[tag=rpg.pseudo_boom.source,limit=1] rpg_boom_id run kill @s
