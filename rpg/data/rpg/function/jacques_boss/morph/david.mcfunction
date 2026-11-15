# 大卫的幽灵出现在最近的玩家身后（原作英雄模型，白色半透明；不能被攻击）
execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated as @e[tag=rpg.unit.f,distance=..1,sort=nearest,limit=1] rotated ~ 0 positioned ^-1.3 ^ ^-1.6 run function rpg:jacques_boss/david/summon
execute unless entity @e[type=minecraft:vindicator,tag=rpg.jqd] positioned ^ ^ ^6 run function rpg:jacques_boss/david/summon
