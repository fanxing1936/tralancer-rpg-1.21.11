# 二阶段打完：倒下（原作倒地动作），火熄灭，约 7 秒后胜利。
function rpg:jacques_boss/refill
tag @s add rpg.jqb.end
scoreboard players set @s rpg_jq_c 0
scoreboard players set @s rpg_jq_sk 0
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
attribute @s minecraft:armor base set 10
kill @e[tag=rpg.jqb.fx]
execute as @e[tag=rpg.jqb.guard] run function rpg:holy_guard/remove
execute as @e[tag=rpg.unit,tag=rpg.jqb.cursed] run function rpg:jacques_boss/curse/clear
function rpg:jacques/weapon/glaive
function rpg:jacques/anim/enter/fall
playsound minecraft:entity.player.death hostile @a[distance=..48] ~ ~ ~ 1.2 0.7
playsound minecraft:block.fire.extinguish hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
bossbar set rpg:jacques_boss value 0
bossbar set rpg:jacques_boss name {"text":"\ue2a0\ue275\ue271\ue279","font":"rpg:jacques_boss"}
