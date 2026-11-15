# 天罚：脚下一枚，走位方向各一枚。
execute at @e[tag=rpg.unit.f,distance=..48,sort=nearest,limit=1] rotated ~ 0 positioned ^ ^ ^ positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/judge
execute at @e[tag=rpg.unit.f,distance=..48,sort=nearest,limit=1] rotated ~ 0 positioned ^ ^ ^5 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/judge
execute at @e[tag=rpg.unit.f,distance=..48,sort=nearest,limit=1] rotated ~ 0 positioned ^4 ^ ^-2 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/judge
execute at @e[tag=rpg.unit.f,distance=..48,sort=nearest,limit=1] rotated ~ 0 positioned ^-4 ^ ^-2 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/judge
