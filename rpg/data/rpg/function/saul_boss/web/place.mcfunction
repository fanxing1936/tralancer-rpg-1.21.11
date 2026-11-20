# 三张蛛网（at 玩家）：脚下、和他的走位方向
function rpg:saul_boss/web/one
execute rotated as @e[tag=rpg.unit.ns,sort=nearest,limit=1] positioned ^ ^ ^3 run function rpg:saul_boss/web/one
execute rotated as @e[tag=rpg.unit.ns,sort=nearest,limit=1] positioned ^2.5 ^ ^1.5 run function rpg:saul_boss/web/one
