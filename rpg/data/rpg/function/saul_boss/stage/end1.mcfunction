# 一阶段打完：甲碎。无敌、站定，约 5 秒后进入二阶段。
function rpg:saul_boss/refill
function rpg:saul_boss/sk/end
tag @s add rpg.slb.morph
scoreboard players set @s rpg_sl_c 0
kill @e[tag=rpg.slb.fx]
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
function rpg:saul/armor/broken
# 碎甲也是特效实体：给它寿命，不然特效计时器把没有分数的实体当成已到期
scoreboard players set @e[tag=rpg.slb.shard,distance=..8] rpg_sl_life 20000
scoreboard players set @e[tag=rpg.slb.shard,distance=..8] rpg_sl_kd 0
function rpg:saul_boss/vfx/shatter
function rpg:saul/anim/enter/kneel
bossbar set rpg:saul_boss value 1000
bossbar set rpg:saul_boss name {"text":"\ue280\ue274\ue270\ue278","font":"rpg:saul_boss"}
