# 二阶段打完：剑从手里滑落，他笑着跪下；约 7 秒后胜利。
function rpg:saul_boss/refill
function rpg:saul_boss/sk/end
tag @s add rpg.slb.end
scoreboard players set @s rpg_sl_c 0
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
kill @e[tag=rpg.slb.fx]
function rpg:saul/anim/enter/kneel
playsound minecraft:entity.player.death hostile @a[distance=..48] ~ ~ ~ 1 0.6
bossbar set rpg:saul_boss value 0
bossbar set rpg:saul_boss name {"text":"\ue2a0\ue275\ue271\ue279","font":"rpg:saul_boss"}
